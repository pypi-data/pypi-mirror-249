from PIL import Image, ImageOps, ImageFilter, ImageEnhance

from .effects import *
from .tools import *

def apply(img: Image, size = (1080, 1080)) -> Image:
    img = ImageOps.exif_transpose(img)
    print("Original size:", img.size)

    # crop
    img_contain = ImageOps.fit(img, size, centering=(0.55, 0.7))    

    # color: +1
    enhancer = ImageEnhance.Color(img_contain)
    img_contain = enhancer.enhance(1.24)

    # brightness
    br = ImageEnhance.Brightness(img_contain)
    img_contain = br.enhance(1.1)

    # sharpness: -3
    img_contain = img_contain.filter(ImageFilter.GaussianBlur(1)) #0.65

    # Contrast
    enh = ImageEnhance.Contrast(img_contain)
    img_contain = enh.enhance(1.6)
    # img_contain = ImageOps.autocontrast(img_contain, 0.65) #0.65

    # Grain
    img_contain = grain(img_contain, 0.02)   

    # POST
    sharper = ImageEnhance.Sharpness(img_contain)
    img_contain = sharper.enhance(1.15)

    enhancer = ImageEnhance.Color(img_contain)
    img_contain = enhancer.enhance(0.8)

    # light leaks    
    liks_preset1 = {"r_max":1000, "intensity":200, 
                    "density":50, "offset":(100,50),
                    "transparency":250, "uselines": False} # Nice
    liks_preset2 = {"r_max":700, "intensity":50, 
                    "density":20, "uselines": True} # rollers trace    
    liks_preset3 = {"r_max":150, "intensity":500, 
                    "density":10, "uselines": True} # rollers trace 2 - more    
    liks_preset4 = {"r_max":150, "intensity":50, 
                    "density":60, "uselines": True} # clear line traces    
    liks_preset5 = {"r_max":100, "intensity":250, 
                    "density":40, "uselines": True} # clear line traces 2 - more

    img_contain = leaks(img_contain, **liks_preset1)    

    #  Tint
    brown = (0.1, -0.01, -0.1)
    red = (0.1, -0.05, -0.1)
    blue = (-0.1, -0.01, 0)
    img_contain = cbalance(img_contain, *brown)
    
    # vignette
    vtype = 1
    
    if vtype == 0:
        #   small rectangle frame
        img_contain = vignette(img_contain, sizep=0.02, transparency=0, 
                            brightness=220, density=60, frame='rect')
    elif vtype == 1:
        #   pale rectangle vignette
        img_contain = vignette(img_contain, sizep=0.01, transparency=0, 
                               brightness=220, density=60, frame='rect') 
    elif vtype == 2:
        #   Nice round vignette
        img_contain = vignette(img_contain, sizep=0.05, transparency=120,
                               brightness=250, density=5, frame="round") 
        
    return img_contain

def open_apply_save(name, orig_path = "orig/", out_path = "out/", suffix="_edit") -> None:
    """Opens file, applies filter, saves the file
    name:
        filename to open
    orig_path:
        where to open
    out_path:
        where to save
    suffix:
        mark outputed filename
    """      
    orig = Image.open(orig_path+name)
    out = apply(orig)

    # save        
    o = out_path+suffixname(name, suffix)
    print("Saving: ", o)
    out.save(o)
    

