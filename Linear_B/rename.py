import os, glob, shutil
from argparse import ArgumentParser 

def get_args():
    parser = ArgumentParser(description = "Filename", add_help = True)
    parser.add_argument('-dir', '--crop_directory', type = str, help = 'Directory with the sign crops', dest = 'DIR', default = os.getcwd())
    parser.add_argument('-out_dir', '--output_directory', type = str, help = 'Output directory', dest = 'OUT_DIR', default = './Renamed')
    return parser.parse_args()

if __name__ == '__main__':
    
    args = get_args()
    crop_dir = args.DIR
    out_dir = args.OUT_DIR
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    tablets_out = list(set([os.path.basename(filename).split('_')[0] for filename in glob.glob(os.path.join(out_dir, '*.png'))]))

    filenames = [os.path.basename(filename).split('.png')[0] for filename in glob.glob(os.path.join(crop_dir, '*.png'))]
    filenames_not_renamed = [filename for filename in filenames if filename.split('_')[0] not in tablets_out]

    tablets = set(map(lambda tab_name:tab_name.split('_')[0], filenames_not_renamed))
    dict_of_tablets = {tab_name: [fnr for fnr in filenames_not_renamed if fnr.split('_')[0] == tab_name] for tab_name in tablets}

    for tab_name in list(dict_of_tablets.keys()):
       
        num_signs = len(dict_of_tablets[tab_name])

        dict_of_signs = {}
        list_rows = sorted(list(set([int(sign.split('_')[1]) - 1 for sign in dict_of_tablets[tab_name]])))
        dict_rows = {row: 0 for row in list_rows}

        for sign in dict_of_tablets[tab_name]:
            
            row = int(sign.split('_')[1]) - 1
            row_id = int(sign.split('_')[2])
            sign_id = sign.split('_', 3)[3]

            new_row_id = str(min(row, 1)*sum(list(dict_rows.values())[:row]) + row_id).zfill(3)

            dict_rows[row] += 1
    
            new_filepath = os.path.join(out_dir, tab_name + '_' + str(row + 1).zfill(3) + '_' + new_row_id + '_' + sign_id + '.png')

            shutil.copy(os.path.join(crop_dir, sign + '.png'), new_filepath)