import os, sys
script_dir = os.path.dirname(os.path.abspath(__file__))

import torch
import pandas as pd
from retro_star.common import prepare_starting_molecules, \
     prepare_molstar_planner, smiles_to_fp
from retro_star.model import ValueMLP
from retro_star.utils import setup_logger
from retroformer.translate import prepare_retroformer, run_retroformer
from utils.ensemble import prepare_ensemble, run_ensemble, prepare_g2s, run_g2s
from retro_star.retriever import Retriever, run_retriever, run_retriever_only, \
    neutralize_atoms, kegg_search, \
    pathRetriever, run_path_retriever, run_both_retriever
from rdkit import Chem


class RSPlanner:
    def __init__(self,
                 cuda=False,
                 beam_size=10,
                 iterations=15,
                 expansion_topk=10,
                 use_value_fn=True,
                 starting_molecules='data/building_block.csv',
                 value_model='retro_star/saved_model/best_epoch_final_4.pt',
                 model_type='ensemble',
                 retrieval_db='data/train_canonicalized.txt',
                 path_retrieval_db='/home/taein/df',
                 kegg_mol_db = "data/kegg_neutral_iso_smi.csv",
                 route_topk=10,
                 retrieval=True,
                 path_retrieval=True,
                 readretro_ckpt_path='.', 
                 g2s_ckpt_path='.'):
        cuda=False
        self.path_retrieve_token = 'keggpath'
        self.kegg_mol_db = pd.read_csv(os.path.join(script_dir,'..',kegg_mol_db))
        self.path_retrieval_db = pd.read_pickle(path_retrieval_db)
        
        setup_logger()
        device = torch.device('cuda' if cuda else 'cpu')
        # device = torch.device('cuda:6' if cuda else 'cpu')
        starting_mols = prepare_starting_molecules(starting_molecules)
        
        model_retroformer, model_g2s, args_retroformer, args_g2s, vocab, vocab_tokens, _ = \
            prepare_ensemble(retroformer_ckpt=readretro_ckpt_path,g2s_ckpt=g2s_ckpt_path,cuda = cuda, beam_size = beam_size, expansion_topk = expansion_topk)
        # print('hi',prepare_ensemble)
        if model_type == "retriever_only":
            starting_mols.add(self.path_retrieve_token)
            path_retriever = pathRetriever(kegg_mol_db, path_retrieval_db, self.path_retrieve_token)
            retriever = Retriever(retrieval_db)
            expansion_handler = lambda x: run_retriever_only(x, path_retriever, retriever)
            
                    
        elif path_retrieval and retrieval:
            starting_mols.add(self.path_retrieve_token)
            path_retriever = pathRetriever(kegg_mol_db, path_retrieval_db, self.path_retrieve_token)
            retriever = Retriever(retrieval_db)
            expansion_handler = lambda x: run_both_retriever(x, path_retriever, retriever, model_type, model_retroformer, model_g2s, args_retroformer, args_g2s,
                                                        vocab, vocab_tokens, device, expansion_topk)
        
        elif path_retrieval and not retrieval:
            starting_mols.add(self.path_retrieve_token)
            path_retriever = pathRetriever(kegg_mol_db, path_retrieval_db, self.path_retrieve_token)
            expansion_handler = lambda x: run_path_retriever(x, path_retriever, model_type, model_retroformer, model_g2s, args_retroformer, args_g2s,
                                                        vocab, vocab_tokens, device, expansion_topk)
        
        elif not path_retrieval and retrieval:
            retriever = Retriever(retrieval_db)
            expansion_handler = lambda x: run_retriever(x, retriever, model_type, model_retroformer, model_g2s, args_retroformer, args_g2s,
                                                        vocab, vocab_tokens, device, expansion_topk)
        else:
            expansion_handler = lambda x: run_ensemble(x, model_type, model_retroformer, model_g2s, args_retroformer, args_g2s,
                                                       vocab, vocab_tokens, device, expansion_topk)

        
        self.top_k = route_topk

        if use_value_fn:
            model = ValueMLP(
                n_layers=1,
                fp_dim=2048,
                latent_dim=128,
                dropout_rate=0.1,
                device=device
            ).to(device)
            model.load_state_dict(torch.load(os.path.join(script_dir,'..',value_model), map_location=device))
            model.eval()
            def value_fn(mol, retrieved):
                if retrieved: return 0.
                fp = smiles_to_fp(mol, fp_dim=2048).reshape(1, -1)
                # print('value_fn')
                fp = torch.FloatTensor(fp).to(device)
                # print(fp)
                # import pdb; pdb.set_trace()
                # print('value_fn',fp,model)
                v = model(fp).item()
                return v
        else:
            value_fn = lambda x, r: 0.
            
        self.plan_handle = prepare_molstar_planner(
            expansion_handler=expansion_handler,
            value_fn=value_fn,
            starting_mols=starting_mols,
            iterations=iterations
        )
    def __keggpath_find(self,routes,token,mol_db,path_db,top_k):
        modi_list = []
        for route in routes[:top_k]:
            r = route.split(">")
            token_position = [i for i,j in enumerate(r) if token in j]
            for pos in token_position:
                cid, _ = kegg_search(neutralize_atoms(r[pos-2].split("|")[-1]),mol_db)
                target_maps = path_db["Map"][path_db['Pathways'].apply(lambda x: any(cid in sublist for sublist in x))].to_list()
                map = target_maps[0]  # check a representation method
                r[pos] = r[pos].replace(token,f'{token}=kegg.jp/pathway/{map}+{cid}')
                if target_maps == []:  # not the case
                    modi_list.append(route)

            modi_route = '>'.join(r)
            modi_list.append(modi_route)
        return modi_list
            
    
    def plan(self, target_mol):
        print("1")
        try:
            target_mol = Chem.MolToSmiles(Chem.MolFromSmiles(target_mol))
            succ, msg = self.plan_handle(target_mol)    # the result of model
            
            if succ:
                routes_list = []
                for route in msg:
                    routes_list.append(route.serialize())
                modi_routes_list = self.__keggpath_find(routes_list,self.path_retrieve_token,self.kegg_mol_db,self.path_retrieval_db,self.top_k)
                return modi_routes_list
            
            elif target_mol != Chem.MolToSmiles(Chem.MolFromSmiles(target_mol),isomericSmiles=False):
                target_mol = Chem.MolToSmiles(Chem.MolFromSmiles(target_mol),isomericSmiles=False)
                succ, msg = self.plan_handle(target_mol)    # the result of model
                if succ:
                    routes_list = []
                    for route in msg:
                        routes_list.append(route.serialize())
                    modi_routes_list = self.__keggpath_find(routes_list,self.path_retrieve_token,self.kegg_mol_db,self.path_retrieval_db,self.top_k)
                    return modi_routes_list
                else:
                    return None
            else:
                return None
        except:
            return None