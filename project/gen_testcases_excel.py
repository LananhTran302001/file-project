import sys
from src.services import read_flows_txt, flows_to_excel
from src.myconstants import INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH

def generate_testcases_from_flows(flows_file_path, testcases_file_path):
    # Doc file usecase -> tra ve flow va cac event 
    flows_and_events = read_flows_txt(flows_file_path)
    flows = flows_and_events["flows"]
    flows_to_excel(flows=flows, excel_file_path=testcases_file_path)

if __name__ == '__main__':
    flows_file_path = INPUT_FOLDER_PATH + sys.argv[1]
    testcases_file_path = OUTPUT_FOLDER_PATH + sys.argv[2]
    generate_testcases_from_flows(flows_file_path, testcases_file_path)