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
		),
	"yellow": ("Magic Guitar",
		"Lulls everyone in the vicinity into a peaceful,",
		"loving state of mind. Also causes large groups",
		"of children to begin making clothing out of",
		"draperies and then sing and frolic in public",
		"places."
		),
	"lime": ("Super Ear Flick of Epic Justice",
		"Just like Mom used to give you, this powerful",
		"device delivers a solid thumping to the upside",
		"of any perpetrators skull, making them immediately",
		"cease whatever misdeeds they might be committing.",
		"May also cause the recipient to feel homesick and",
		"vaguely guilty."
		),
	"green": ("Costume Glasses",
		"Got to protect that secret identity! Comes only",
		"in black plastic frame models. Can be upgraded to",
		"reflective models that prevent accidental laser",
		"eyes for an additional fee."
		),
	"aqua": ("Extra Strength Whitening Toothpaste",
		"For that pearly white superhero smile. As a bonus,",
		"can also be used to blind your opponents."
		),
	"blue": ("Lens Flare",
		"So shiny! Certain to be good for making an entrance!"
		),
	"purple": ("Sidekick in a Box",
		"Just add water! Tragic backstory not included."
		),
	"pink": None,
	"brown": None,
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
	"yellow": ("Call Me Maybe",
		"Makes everyone's cell phone ring at once,",
		"distracting them and annoying them at the",
		"same time!"
		),
	"lime": ("iJerk",
		"Charges the villain's smartphone by draining",
		"all the phone batteries in the vicinity."
		),
	"green": ("Evil Laugh Generator",
		"Useful for when you have a sore throat, or",
		"if you haven't quite perfected your own",
		"villainous chuckle just yet."
		),
	"aqua": ("Ramen Noodle Net",
		"Disguised as an innocent package of inexpensive",
		"foodstuffs, this device is great for capturing",
		"cash-strapped superheroes and college students."
		),
	"blue": ("X-Ray Goggles",
		"For seeing inside bank vaults, secured locations,",
		"etc. Only for the purposes of doing generically",
		"evil deeds; after all, even villains have standards."
		),
	"purple": ("Grow your own Minions",
		"Just empty the packet into a tank of water,",
		"add some patented Minion food everyday, and wait...",
		"You'll see minions within a week! Minions can be",
		"trained to follow your orders* and do amazing things!",
		"",
		"*Company is not responsible for customer",
		"  dissatisfaction with Minions"
		),
	"pink": None,
	"brown": None,
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
	"yellow": ("Giant Banana",
		"Good for light maiming *AND* demoralizing!"
		),
	"lime": ("Velcro Cape Lining",
		"For obvious reasons."
		),
	"green": ("Stealth Vehicle",
		"Cleverly disguised as an ordinary bicycle, this",
		"manually powered energy efficient vehicle is perfect",
		"whether you're chasing the bad guys or making a",
		"quick getaway! Includes a small bell and a basket",
		"for convenient storage."
		),
	"aqua": ("Extreme Energy Caffeine Bars",
		"Tired from a long night on the streets of",
		"Metropolistuckiland? Need to recharge that energy",
		"bar? Look no further! Side effects may include",
		"uncontrollable shaking, jittery flight, and",
		"supersonic speech."
		),
	"blue": ("Police Scanner",
		"What? It's practical!"
		),
	"purple": ("Insignia Kit",
		"Customizable logo for the front of your costume."
		),
	"pink": None,
	"brown": None,
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