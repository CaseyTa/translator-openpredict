import datetime
import logging
import os
import shutil
import time
from pathlib import Path

import pandas as pd
import pkg_resources
import requests
from gensim.models import KeyedVectors
from joblib import load
from openpredict.config import settings

MISSING_IDS = set()


def log(msg: str):
    """Simple print with a timestamp"""
    log_msg = '[' + str(datetime.datetime.now().strftime("%Y-%m-%d@%H:%M:%S")) + '] ' + msg 
    # logging.info(log_msg)
    print(log_msg)


def get_openpredict_dir(subfolder=''):
    """Return the full path to the provided files in the OpenPredict data folder
    Where models and features for runs are stored
    """
    if not settings.OPENPREDICT_DATA_DIR.endswith('/'):
        settings.OPENPREDICT_DATA_DIR += '/'
    return settings.OPENPREDICT_DATA_DIR + subfolder



def init_openpredict_dir():
    """Create OpenPredict folder and initiate files if necessary."""

    print('Using directory: ' + settings.OPENPREDICT_DATA_DIR)
    print('Creating if does not exist: ' + get_openpredict_dir())
    Path(get_openpredict_dir()).mkdir(parents=True, exist_ok=True)
    print('Creating if does not exist: ' + get_openpredict_dir('features'))
    Path(get_openpredict_dir('features')).mkdir(parents=True, exist_ok=True)
    print('Creating if does not exist: ' + get_openpredict_dir('models'))
    Path(get_openpredict_dir('models')).mkdir(parents=True, exist_ok=True)
    print('Creating if does not exist: ' + get_openpredict_dir('kgpredict'))
    Path(get_openpredict_dir('kgpredict')).mkdir(parents=True, exist_ok=True)
    print('Creating if does not exist: ' + get_openpredict_dir('xpredict'))
    Path(get_openpredict_dir('xpredict')).mkdir(parents=True, exist_ok=True)

    if not os.path.exists(get_openpredict_dir('features/openpredict-baseline-omim-drugbank.joblib')):
        print('Initiating ' + get_openpredict_dir('features/openpredict-baseline-omim-drugbank.joblib'))
        shutil.copy(pkg_resources.resource_filename('openpredict', 'data/features/openpredict-baseline-omim-drugbank.joblib'),
            get_openpredict_dir('features/openpredict-baseline-omim-drugbank.joblib'))
    if not os.path.exists(get_openpredict_dir('models/openpredict-baseline-omim-drugbank.joblib')):
        print('Initiating ' + get_openpredict_dir('models/openpredict-baseline-omim-drugbank.joblib'))
        shutil.copy(pkg_resources.resource_filename('openpredict', 'data/models/openpredict-baseline-omim-drugbank.joblib'), 
            get_openpredict_dir('models/openpredict-baseline-omim-drugbank.joblib'))
    if not os.path.exists(get_openpredict_dir('openpredict-metadata.ttl')):
        print('Creating ' + get_openpredict_dir('openpredict-metadata.ttl'))
        # shutil.copy(get_openpredict_dir('initial-openpredict-metadata.ttl'), 
        shutil.copy(pkg_resources.resource_filename('openpredict', 'data/openpredict-metadata.ttl'), 
            get_openpredict_dir('openpredict-metadata.ttl'))


    if not os.path.exists(get_openpredict_dir('kgpredict/kgpredict_drug_diseasemappings.tsv')):
        print('Initiating ' + get_openpredict_dir('kgpredict/kgpredict_drug_diseasemappings.tsv'))
        shutil.copy(pkg_resources.resource_filename('openpredict', 'data/kgpredict/kgpredict_drug_diseasemappings.tsv'), 
            get_openpredict_dir('kgpredict/kgpredict_drug_diseasemappings.tsv'))

    if not os.path.exists(get_openpredict_dir('xpredict/deepdrug_repurposingpredictiondataset.csv')):
        print('Initiating ' + get_openpredict_dir('xpredict/deepdrug_repurposingpredictiondataset.csv'))
        shutil.copy(pkg_resources.resource_filename('openpredict', 'data/xpredict/deepdrug_repurposingpredictiondataset.csv'),
            get_openpredict_dir('xpredict/deepdrug_repurposingpredictiondataset.csv'))

    if not os.path.exists(get_openpredict_dir('kgpredict/embed/entity_embeddings.npy')):
        print(f"📥️ Downloading Drug Repurposing KG embeddings in {get_openpredict_dir('kgpredict/embed')}")
        os.system('wget -q --show-progress purl.org/kgpredict -O /tmp/kgpredictfiles.tar.gz')
        os.system(f"tar -xzvf /tmp/kgpredictfiles.tar.gz  -C {get_openpredict_dir('kgpredict')}")
        os.rename(get_openpredict_dir('kgpredict/embed/DRKG_TransE_l2_entity.npy'), get_openpredict_dir('kgpredict/embed/entity_embeddings.npy'))
        os.rename(get_openpredict_dir('kgpredict/embed/DRKG_TransE_l2_relation.npy'), get_openpredict_dir('kgpredict/embed/relation_embeddings.npy'))

        # shutil.copy(pkg_resources.resource_filename('openpredict', 'data/features/openpredict-baseline-omim-drugbank.joblib'),
        #     get_openpredict_dir('features/openpredict-baseline-omim-drugbank.joblib'))

    print('✅ OpenPredict data initialized')

# echo `pwd` > pwdfile.txt
# #download kg predict drugrepurposing files
# wget -q --show-progress purl.org/kgpredict -O kgpredictfiles.tar.gz
# #extract kgpredict files

# tar -xzvf kgpredictfiles.tar.gz  -C ./openpredict/data/kgpredict/
# rm kgpredictfiles.tar.gz

# mv ./openpredict/data/kgpredict/embed/DRKG_TransE_l2_entity.npy ./openpredict/data/kgpredict/embed/entity_embeddings.npy
# mv ./openpredict/data/kgpredict/embed/DRKG_TransE_l2_relation.npy ./openpredict/data/kgpredict/embed/relation_embeddings.npy



    
    # attempts = 0
    # while attempts < 30:
    #     try:
    #         init_triplestore()
    #         break
    #     except Exception as e:
    #         print(e)
    #         print('Failed to connect to the SPARQL endpoint, attempt ' + str(attempts))
    #         time.sleep(5)
    #         attempts += 1
    # Check if https://w3id.org/openpredict/run/openpredict-baseline-omim-drugbank exist before iniating the triplestore
    # add_feature_metadata("GO-SIM", "GO based drug-drug similarity", "Drugs")
    # add_feature_metadata("TARGETSEQ-SIM", "Drug target sequence similarity: calculation of SmithWaterman sequence alignment scores", "Drugs")
    # add_feature_metadata("PPI-SIM", "PPI based drug-drug similarity, calculate distance between drugs on protein-protein interaction network", "Drugs")
    # add_feature_metadata("TC", "Drug fingerprint similarity, calculating MACS based fingerprint (substructure) similarity", "Drugs")
    # add_feature_metadata("SE-SIM", "Drug side effect similarity, calculating Jaccard coefficient based on drug sideefects", "Drugs")
    # add_feature_metadata("PHENO-SIM", "Disease Phenotype Similarity based on MESH terms similarity", "Diseases")
    # add_feature_metadata("HPO-SIM", "HPO based disease-disease similarity", "Diseases")



def get_entities_labels(entity_list):
    """Send the list of node IDs to Translator Normalization API to get labels
    See API: https://nodenormalization-sri.renci.org/apidocs/#/Interfaces/get_get_normalized_nodes
    and example notebook: https://github.com/TranslatorIIPrototypes/NodeNormalization/blob/master/documentation/NodeNormalization.ipynb
    """
    # TODO: add the preferred identifier CURIE to our answer also?
    try:
        get_label_result = requests.get('https://nodenormalization-sri.renci.org/get_normalized_nodes',
                            params={'curie': entity_list})
        get_label_result = get_label_result.json()
    except:
        # Catch if the call to the API fails (API not available)
        logging.info("Translator API down: https://nodenormalization-sri.renci.org/apidocs")
        get_label_result = {}
    # Response is a JSON:
    # { "HP:0007354": {
    #     "id": { "identifier": "MONDO:0004976",
    #       "label": "amyotrophic lateral sclerosis" },
    return get_label_result

def normalize_id_to_translator(ids_list):
    """Use Translator SRI NodeNormalization API to get the preferred Translator ID
    for an ID https://nodenormalization-sri.renci.org/docs
    """
    converted_ids_obj = {}
    resolve_curies = requests.get('https://nodenormalization-sri.renci.org/get_normalized_nodes',
                    params={'curie': ids_list})
    # Get corresponding OMIM IDs for MONDO IDs if match
    resp = resolve_curies.json()
    # print(resp)
    for converted_id, translator_ids in resp.items():
        try:
            pref_id = translator_ids['id']['identifier']
            print(converted_id + ' > ' + pref_id)
            converted_ids_obj[converted_id] = pref_id
        except:
            print('❌️ ' + converted_id + ' > ' + str(translator_ids))

    return converted_ids_obj

def convert_baseline_features_ids():
    """Convert IDs to use Translator preferred IDs when building the baseline model from scratch"""
    baseline_features_folder = "data/baseline_features/"
    drugfeatfiles = ['drugs-fingerprint-sim.csv','drugs-se-sim.csv', 
                    'drugs-ppi-sim.csv', 'drugs-target-go-sim.csv','drugs-target-seq-sim.csv']
    diseasefeatfiles =['diseases-hpo-sim.csv',  'diseases-pheno-sim.csv' ]
    drugfeatfiles = [ pkg_resources.resource_filename('openpredict', os.path.join(baseline_features_folder, fn)) for fn in drugfeatfiles]
    diseasefeatfiles = [ pkg_resources.resource_filename('openpredict', os.path.join(baseline_features_folder, fn)) for fn in diseasefeatfiles]

    # Prepare drug-disease dictionary
    drugDiseaseKnown = pd.read_csv(pkg_resources.resource_filename('openpredict', 'data/resources/openpredict-omim-drug.csv'),delimiter=',') 
    drugDiseaseKnown.rename(columns={'drugid':'Drug','omimid':'Disease'}, inplace=True)
    drugDiseaseKnown.Disease = drugDiseaseKnown.Disease.astype(str)

    drugs_set = set()
    diseases_set = set()
    drugs_set.update(drugDiseaseKnown['Drug'].tolist())
    diseases_set.update(drugDiseaseKnown['Disease'].tolist())

    for csv_file in drugfeatfiles:
        df = pd.read_csv(csv_file, delimiter=',')
        drugs_set.update(df['Drug1'].tolist())
        drugs_set.update(df['Drug2'].tolist())

    for csv_file in diseasefeatfiles:
        df = pd.read_csv(csv_file, delimiter=',')
        diseases_set.update(df['Disease1'].tolist())
        diseases_set.update(df['Disease2'].tolist())
    
    diseases_set = ['OMIM:{0}'.format(disease) for disease in diseases_set]
    drugs_set = ['DRUGBANK:{0}'.format(drug) for drug in drugs_set]

    diseases_mappings = normalize_id_to_translator(diseases_set)
    drugs_mappings = normalize_id_to_translator(drugs_set)

    print('Finished API queries')
    # Replace Ids with translator IDs in kown drug disease associations
    drugDiseaseKnown["Drug"] = drugDiseaseKnown["Drug"].apply (lambda row: map_id_to_translator(drugs_mappings, 'DRUGBANK:' + row)     )
    drugDiseaseKnown["Disease"] = drugDiseaseKnown["Disease"].apply (lambda row: map_id_to_translator(diseases_mappings, 'OMIM:' + str(row)) )
    drugDiseaseKnown.to_csv('openpredict/data/resources/known-drug-diseases.csv', index=False)

    # Replace IDs in drugs baseline features files
    for csv_file in drugfeatfiles:
        df = pd.read_csv(csv_file, delimiter=',')
        df["Drug1"] = df["Drug1"].apply (lambda row: map_id_to_translator(drugs_mappings, 'DRUGBANK:' + row) )
        df["Drug2"] = df["Drug2"].apply (lambda row: map_id_to_translator(drugs_mappings, 'DRUGBANK:' + row) )
        df.to_csv(csv_file.replace('/baseline_features/', '/translator_features/'), index=False)

    # Replace IDs in diseases baseline features files
    for csv_file in diseasefeatfiles:
        df = pd.read_csv(csv_file, delimiter=',')
        df["Disease1"] = df["Disease1"].apply (lambda row: map_id_to_translator(diseases_mappings, 'OMIM:' + str(row)) )
        df["Disease2"] = df["Disease2"].apply (lambda row: map_id_to_translator(diseases_mappings, 'OMIM:' + str(row)) )
        df.to_csv(csv_file.replace('/baseline_features/', '/translator_features/'), index=False)

    print('❌️ Missing IDs: ')
    for missing_id in MISSING_IDS:
        print(missing_id)
    

    # drugs_set.add(2)
    # drugs_set.update([2, 3, 4])

    # Extract the dataframes col1 and 2 to a unique list
    # Add those list to the drugs and diseases sets
    # Convert the set/list it using normalize_id_to_translator(ids_list)
    # Update all dataframes using the created mappings
    # And store to baseline_translator

def map_id_to_translator(mapping_obj, source_id):
    try:
        return mapping_obj[source_id]
    except:
        MISSING_IDS.add(source_id)
        return source_id



def load_similarity_embeddings():
    """Load embeddings model for similarity"""
    embedding_folder = 'data/embedding'
    # print(pkg_resources.resource_filename('openpredict', embedding_folder))
    similarity_embeddings = {}
    for model_id in os.listdir(pkg_resources.resource_filename('openpredict', embedding_folder)):
        if model_id.endswith('txt'):
            feature_path = pkg_resources.resource_filename('openpredict', os.path.join(embedding_folder, model_id))
            print("📥 Loading similarity features from " + feature_path)
            emb_vectors = KeyedVectors.load_word2vec_format(feature_path)
            similarity_embeddings[model_id]= emb_vectors
    return similarity_embeddings


def load_treatment_classifier(model_id):
    """Load embeddings model for treats and treated_by"""
    print("📥 Loading treatment classifier from joblib for model " + str(model_id))
    return load(f'{settings.OPENPREDICT_DATA_DIR}/models/{str(model_id)}.joblib')


def load_treatment_embeddings(model_id):
    """Load embeddings model for treats and treated_by"""
    print(f"📥 Loading treatment features for model {str(model_id)}")
    (drug_df, disease_df) = load(f'{settings.OPENPREDICT_DATA_DIR}/features/{str(model_id)}.joblib')
    return (drug_df, disease_df)

