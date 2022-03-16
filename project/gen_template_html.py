import sys
from src.services import read_flows_txt, flow_to_html
from src.myconstants import INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH

def generate_template_html_from_flows(flows_file_path, html_file_path):
    # Doc file usecase -> tra ve flow va cac event 
    flows_and_events = read_flows_txt(flows_file_path)
    flows = flows_and_events["flows"]
    flow_to_html(flow=flows[0], html_file_path=html_file_path)

if __name__ == '__main__':
    flow_file_path = INPUT_FOLDER_PATH + sys.argv[1]
    html_file_path = OUTPUT_FOLDER_PATH + sys.argv[2]
    generate_template_html_from_flows(flow_file_path, html_file_path)