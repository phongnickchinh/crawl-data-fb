#lướt qua các tệp trong thư mục, nêu tệp nhỏ hơn 50kb thì xóa
import os
def delete_small_files(input_folder, minimum_size = 50000):
    for file in os.listdir(input_folder):
        print("Processing: ", file)
        if os.path.getsize(input_folder + "/" + file) < minimum_size:
            os.remove(input_folder + "/" + file)
            print("Deleted: ", file)
        print("\n")
    print("Done")