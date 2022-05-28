from PIL import Image
import os

#Open images and reduce quality, then samve
def reduce_res(target_folder, newdir):
    total_files = len(os.listdir(target_folder))
    i = 1
    for filename in os.listdir(target_folder):
        print("Image", i, "of", total_files, "in", target_folder)
        i += 1
        image_file = Image.open(target_folder + "/" + filename)
        # Changing the image resolution using quality parameter
        new_filename = newdir + "/" + filename
        new_filename = new_filename.replace(".png", ".jpg")
        print("Saving to ", new_filename, "...", sep = "")
        new_img = open(new_filename, "a")
        image_file.save(new_filename, dpi = (300,300))

if __name__ == "__main__":
    #training images
    print("Reducing quality of files in train folder...\n")
    reduce_res("oldtrain2017", "train2017")
    print("Reducing quality of files in val folder...\n")
    reduce_res("oldval2017", "val2017")
    print("Reducing quality of files in test folder...\n")
    reduce_res("oldtest2017", "test2017")



