HERO_PRODUCTS = {
	"red": ("Super Strength Hair Spray",
		"Because all that flying around isn't good",
		"for your style. Also can be used as super",
		"glue in a pinch. Just don't get too close",
		"to any open flames."
		),
	"orange": ("The 2000XL Kitten Extractor",
		"The very latest and most high tech method",
		"of securing small felines from large woody",
		"perennials. Please read owner's manual",
		"before operating this complex machinery.",
		"No refunds in cases of dismemberment."
		)
}

VILLAIN_PRODUCTS = {
	"red": ("Stair Master",
		"Makes all escalators in the area stop",
		"working. Not one of the best ideas in",
		"villainy."
		),
	"orange": ("Automated Puppy Kicker",
		"Because sometimes you just don't have",
		"time for those simple pleasures."
		),
}

NEUTRAL_PRODUCTS = {
	"red": ("Rubber Suit",
		"Whatever you throw bounces off me and",
		"hits you! Not recommended for use in",
		"racquetball courts."
		),
	"orange": ("Helium Gun",
		"Makes your enemy talk funny. No one",
		"takes them seriously, and they go home",
		"in shame."
		),
}

def get_product(key):
	p, c = key.split('_')
	lookup = None
	if p == 'h':
		lookup = HERO_PRODUCTS
	elif p == 'v':
		lookup = VILLAIN_PRODUCTS
	else:
		lookup = NEUTRAL_PRODUCTS
	
	output = lookup.get(c)
	
	if output != None:
		title = output[0]
		description = output[1:]
	else:
		title = "Untitled Product"
		description = ["Please add a description in Products.py"]
	
	return (title, description)