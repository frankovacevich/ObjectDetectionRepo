import helperCV2 as img
import random
import os
import sys

imageblack = img.readImg("DECK/back.png")
i_write = 0 #Index for writing the images

def GenerateSet(set_name = "train", Nbackgrounds = 60, Nsingle = 3, Npairs = 3, Ntrios = 1):

    # There are many backgrounds to choose from -> N_backgrounds
    # At first for each background N_single pictures with each card (there are 54 cards) -> N_single
    # Then for each background we want a picture with two cards randomly picked -> N_two_cards
    #
    # The set will have N_backgrounds * (N_single * #Cards + N_pairs + N_trios) pictures

    N_backgrounds = Nbackgrounds  # Number of backgrounds
    N_single = Nsingle
    N_pairs = Npairs
    N_trios = Ntrios

    CARD_IMAGES = get_card_image_set()

    TotalNumberOfBackgrounds = 5640
    StepSize = int(TotalNumberOfBackgrounds / N_backgrounds)
    i = 0
    with open("BACKGROUNDS/labels/test1.txt") as background_list:
        for line in background_list:
            i += 1
            if i != StepSize:
                continue
            i = 0

            line = line.replace("\n","")
            background_image = img.readImg("BACKGROUNDS/images/" + line)

            ##GENERATE SINGLE SET
            for card in CARD_IMAGES:
                for j in range(0, N_single):
                    image,rectangle = place_card_at_random_position(background_image,card[1])
                    #img.displayImg(image,[rectangle])
                    rectangle.append(card[0])
                    save_image_and_label(image, [rectangle], set_name)

            ##GENERATE PAIR SET
            for j in range(0, N_pairs):
                card1 = CARD_IMAGES[random.randint(0, len(CARD_IMAGES) - 1)]
                card2 = CARD_IMAGES[random.randint(0, len(CARD_IMAGES) - 1)]
                image, rectangle1 = place_card_at_random_position(background_image, card1[1])
                image, rectangle2 = place_card_at_random_position(image, card2[1])
                #img.displayImg(image,[rectangle1,rectangle2])
                rectangle1.append(card1[0])
                rectangle2.append(card2[0])
                save_image_and_label(image, [rectangle1, rectangle2], set_name)

            ##GENERATE TRIO SET
            for j in range(0, N_trios):
                card1 = CARD_IMAGES[random.randint(0, len(CARD_IMAGES) - 1)]
                card2 = CARD_IMAGES[random.randint(0, len(CARD_IMAGES) - 1)]
                card3 = CARD_IMAGES[random.randint(0, len(CARD_IMAGES) - 1)]
                image, rectangle1 = place_card_at_random_position(background_image, card1[1])
                image, rectangle2 = place_card_at_random_position(image, card2[1])
                image, rectangle3 = place_card_at_random_position(image, card3[1])
                #img.displayImg(image, [rectangle1, rectangle2, rectangle3])
                rectangle1.append(card1[0])
                rectangle2.append(card2[0])
                rectangle3.append(card3[0])
                save_image_and_label(image, [rectangle1, rectangle2, rectangle3], set_name)

def save_image_and_label(image, rectangles,set_name):
    global i_write
    i_write += 1
    filename = "IMG_" + str(i_write)
    img.saveToFile(image, set_name + "/" + filename + ".png")
    w,h,c = img.getImgSize(image)

    metadata =  "file: " + "ObjectDetectionRepo/images/" + set_name + "/" + filename + ".png"
    metadata += "\nwidth: " + str(w)
    metadata += "\nheight: " + str(h)

    for rectangle in rectangles:
        metadata += "\n" + "class: " + rectangle[4]
        metadata += "\n" + "xmin: " + str(rectangle[0])
        metadata += "\n" + "xmax: " + str(rectangle[1])
        metadata += "\n" + "ymin: " + str(rectangle[2])
        metadata += "\n" + "ymax: " + str(rectangle[3])

    f_out = open(set_name + "/" + filename + ".txt","w+",encoding="UTF8")
    f_out.write(metadata)
    f_out.close()
    print(i_write)

def place_card_at_random_position(background_image, card_image):
    """
    Places a card at random position on the background
    Returns the final image and the position of the card placed (result_image, (xmin, xmax, ymin, ymax))
    """
    w,h,c = img.getImgSize(card_image)
    W,H,C = img.getImgSize(background_image)
    scale_factor = 0.55 * H/h

    card_image = img.placeImg(card_image,imageblack,0,0)
    card_image = img.scaleImg(card_image,scale_factor)
    card_image = img.rotateImg(card_image,random.randint(0,360))

    w, h, c = img.getImgSize(card_image)
    xmin = random.randint(0,W-w)
    ymin = random.randint(0,H-h)
    xmax = xmin + w
    ymax = ymin + h

    output = img.placeImg(card_image, background_image, xmin, ymin)
    output = img.adjustGamma(output, random.uniform(0.5,2.5))

    return (output, [xmin, xmax, ymin, ymax])

def get_card_image_set():
    """
    Returns a vector with the images of all the cards:
              vector of tuples (class, image)
    """
    CARD_IMAGES = []
    for file in os.listdir("ObjectedDetectionRepo/images/DECK"):
        if not file == "back.png":
            CARD_IMAGES.append((remove_extension(file), img.readImg("DECK/" + file)))
    return CARD_IMAGES

def remove_extension(file):
    return file[:file.rfind(".")]


argc = len(sys.argv)
argv = sys.argv

print("")
print("Function GenerateSet ( set_name , Nbackground , Nsingles , Npairs , Ntrios )")
print("")

if argc == 1:
    GenerateSet()
elif argc == 2:
    GenerateSet(argv[1])
elif argc == 6:
    GenerateSet(argv[1],int(argv[2]),int(argv[3]),int(argv[4]),int(argv[5]))



