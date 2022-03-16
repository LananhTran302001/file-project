import sys
from src.services import read_usecases_txt, flows_to_txt
from src.myconstants import INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH

def generate_flows_from_usecases(usecases_file_path, flows_file_path):
    # Doc file usecase -> tra ve flow va cac event 
    flows_and_events = read_usecases_txt(usecases_file_path)
    flows = flows_and_events["flows"]
    flows_to_txt(flows=flows, txt_file_path=flows_file_path)

if __name__ == '__main__':
    usecases_file_path = INPUT_FOLDER_PATH + sys.argv[1]
    flows_file_path = OUTPUT_FOLDER_PATH + sys.argv[2]
    generate_flows_from_usecases(usecases_file_path, flows_file_path)