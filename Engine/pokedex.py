import pokemon

class Template:
	def __init__(self, num, species, elements, gender_ratios, base_stats):
		self.num = num
		self.species = species
		self.elements = elements
		self.gender_ratios = gender_ratios
		self.base_hp = base_stats[0]
		self.base_atk = base_stats[1]
		self.base_def = base_stats[2]
		self.base_spa = base_stats[3]
		self.base_spd = base_stats[4]
		self.base_spe = base_stats[5]

pokedex_list = {
"BULBASAUR" : Template(1,"Bulbasaur",["GRASS","POISON"],[0.875,0.125,0],[45,49,49,65,65,45]),
"IVYSAUR" : Template(2,"Ivysaur",["GRASS","POISON"],[0.875,0.125,0],[60,62,63,80,80,60]),
"VENUSAUR" : Template(3,"Venusaur",["GRASS","POISON"],[0.875,0.125,0],[80,82,83,100,100,80]),
"CHARMANDER" : Template(4,"Charmander",["FIRE"],[0.875,0.125,0],[39,52,43,50,50,65]),
"CHARMELEON" : Template(5,"Charmeleon",["FIRE"],[0.875,0.125,0],[58,64,58,65,65,80]),
"CHARIZARD" : Template(6,"Charizard",["FIRE","FLYING"],[0.875,0.125,0],[78,84,78,85,85,100]),
"SQUIRTLE" : Template(7,"Squirtle",["WATER"],[0.875,0.125,0],[44,48,65,50,50,43]),
"WARTORTLE" : Template(8,"Wartortle",["WATER"],[0.875,0.125,0],[59,63,80,65,65,58]),
"BLASTOISE" : Template(9,"Blastoise",["WATER"],[0.875,0.125,0],[79,83,100,85,85,78]),
"CATERPIE" : Template(10,"Caterpie",["BUG"],[0.5,0.5,0],[45,30,35,20,20,45]),
"METAPOD" : Template(11,"Metapod",["BUG"],[0.5,0.5,0],[50,20,55,25,25,30]),
"BUTTERFREE" : Template(12,"Butterfree",["BUG","FLYING"],[0.5,0.5,0],[60,45,50,80,80,70]),
"WEEDLE" : Template(13,"Weedle",["BUG","POISON"],[0.5,0.5,0],[40,35,30,20,20,50]),
"KAKUNA" : Template(14,"Kakuna",["BUG","POISON"],[0.5,0.5,0],[45,25,50,25,25,35]),
"BEEDRILL" : Template(15,"Beedrill",["BUG","POISON"],[0.5,0.5,0],[65,80,40,45,45,75]),
"PIDGEY" : Template(16,"Pidgey",["NORMAL","FLYING"],[0.5,0.5,0],[40,45,40,35,35,56]),
"PIDGEOTTO" : Template(17,"Pidgeotto",["NORMAL","FLYING"],[0.5,0.5,0],[63,60,55,50,50,71]),
"PIDGEOT" : Template(18,"Pidgeot",["NORMAL","FLYING"],[0.5,0.5,0],[83,80,75,70,70,91]),
"RATTATA" : Template(19,"Rattata",["NORMAL"],[0.5,0.5,0],[30,56,35,25,25,72]),
"RATICATE" : Template(20,"Raticate",["NORMAL"],[0.5,0.5,0],[55,81,60,50,50,97]),
"SPEAROW" : Template(21,"Spearow",["NORMAL","FLYING"],[0.5,0.5,0],[40,60,30,31,31,70]),
"FEAROW" : Template(22,"Fearow",["NORMAL","FLYING"],[0.5,0.5,0],[65,90,65,61,61,100]),
"EKANS" : Template(23,"Ekans",["POISON"],[0.5,0.5,0],[35,60,44,40,40,55]),
"ARBOK" : Template(24,"Arbok",["POISON"],[0.5,0.5,0],[60,85,69,65,65,80]),
"PIKACHU" : Template(25,"Pikachu",["ELECTRIC"],[0.5,0.5,0],[35,55,30,50,50,90]),
"RAICHU" : Template(26,"Raichu",["ELECTRIC"],[0.5,0.5,0],[60,90,55,90,90,110]),
"SANDSHREW" : Template(27,"Sandshrew",["GROUND"],[0.5,0.5,0],[50,75,85,30,30,40]),
"SANDSLASH" : Template(28,"Sandslash",["GROUND"],[0.5,0.5,0],[75,100,110,55,55,65]),
"NIDORANF" : Template(29,"Nidoran-F",["POISON"],[0,1,0],[55,47,52,40,40,41]),
"NIDORINA" : Template(30,"Nidorina",["POISON"],[0,1,0],[70,62,67,55,55,56]),
"NIDOQUEEN" : Template(31,"Nidoqueen",["POISON","GROUND"],[0,1,0],[90,82,87,75,75,76]),
"NIDORANM" : Template(32,"Nidoran-M",["POISON"],[1,0,0],[46,57,40,40,40,50]),
"NIDORINO" : Template(33,"Nidorino",["POISON"],[1,0,0],[61,72,57,55,55,65]),
"NIDOKING" : Template(34,"Nidoking",["POISON","GROUND"],[1,0,0],[81,92,77,75,75,85]),
"CLEFAIRY" : Template(35,"Clefairy",["NORMAL"],[0.25,0.75,0],[70,45,48,60,60,35]),
"CLEFABLE" : Template(36,"Clefable",["NORMAL"],[0.25,0.75,0],[95,70,73,85,85,60]),
"VULPIX" : Template(37,"Vulpix",["FIRE"],[0.25,0.75,0],[38,41,40,65,65,65]),
"NINETALES" : Template(38,"Ninetales",["FIRE"],[0.25,0.75,0],[73,76,75,100,100,100]),
"JIGGLYPUFF" : Template(39,"Jigglypuff",["NORMAL"],[0.25,0.75,0],[115,45,20,25,25,20]),
"WIGGLYTUFF" : Template(40,"Wigglytuff",["NORMAL"],[0.25,0.75,0],[140,70,45,50,50,45]),
"ZUBAT" : Template(41,"Zubat",["POISON","FLYING"],[0.5,0.5,0],[40,45,35,40,40,55]),
"GOLBAT" : Template(42,"Golbat",["POISON","FLYING"],[0.5,0.5,0],[75,80,70,75,75,90]),
"ODDISH" : Template(43,"Oddish",["GRASS","POISON"],[0.5,0.5,0],[45,50,55,75,75,30]),
"GLOOM" : Template(44,"Gloom",["GRASS","POISON"],[0.5,0.5,0],[60,65,70,85,85,40]),
"VILEPLUME" : Template(45,"Vileplume",["GRASS","POISON"],[0.5,0.5,0],[75,80,85,100,100,50]),
"PARAS" : Template(46,"Paras",["BUG","GRASS"],[0.5,0.5,0],[35,70,55,55,55,25]),
"PARASECT" : Template(47,"Parasect",["BUG","GRASS"],[0.5,0.5,0],[60,95,80,80,80,30]),
"VENONAT" : Template(48,"Venonat",["BUG","POISON"],[0.5,0.5,0],[60,55,50,40,40,45]),
"VENOMOTH" : Template(49,"Venomoth",["BUG","POISON"],[0.5,0.5,0],[70,65,60,90,90,90]),
"DIGLETT" : Template(50,"Diglett",["GROUND"],[0.5,0.5,0],[10,55,25,45,45,95]),
"DUGTRIO" : Template(51,"Dugtrio",["GROUND"],[0.5,0.5,0],[35,80,50,70,70,120]),
"MEOWTH" : Template(52,"Meowth",["NORMAL"],[0.5,0.5,0],[40,45,35,40,40,90]),
"PERSIAN" : Template(53,"Persian",["NORMAL"],[0.5,0.5,0],[65,70,60,65,65,115]),
"PSYDUCK" : Template(54,"Psyduck",["WATER"],[0.5,0.5,0],[50,52,48,50,50,55]),
"GOLDUCK" : Template(55,"Golduck",["WATER"],[0.5,0.5,0],[80,82,78,80,80,85]),
"MANKEY" : Template(56,"Mankey",["FIGHTING"],[0.5,0.5,0],[40,80,35,35,35,70]),
"PRIMEAPE" : Template(57,"Primeape",["FIGHTING"],[0.5,0.5,0],[65,105,60,60,60,95]),
"GROWLITHE" : Template(58,"Growlithe",["FIRE"],[0.75,0.25,0],[55,70,45,50,50,60]),
"ARCANINE" : Template(59,"Arcanine",["FIRE"],[0.75,0.25,0],[90,110,80,80,80,95]),
"POLIWAG" : Template(60,"Poliwag",["WATER"],[0.5,0.5,0],[40,50,40,40,40,90]),
"POLIWHIRL" : Template(61,"Poliwhirl",["WATER"],[0.5,0.5,0],[65,65,65,50,50,90]),
"POLIWRATH" : Template(62,"Poliwrath",["WATER","FIGHTING"],[0.5,0.5,0],[90,85,95,70,70,70]),
"ABRA" : Template(63,"Abra",["PSYCHIC"],[0.75,0.25,0],[25,20,15,105,105,90]),
"KADABRA" : Template(64,"Kadabra",["PSYCHIC"],[0.75,0.25,0],[40,35,30,120,120,105]),
"ALAKAZAM" : Template(65,"Alakazam",["PSYCHIC"],[0.75,0.25,0],[55,50,45,135,135,120]),
"MACHOP" : Template(66,"Machop",["FIGHTING"],[0.75,0.25,0],[70,80,50,35,35,35]),
"MACHOKE" : Template(67,"Machoke",["FIGHTING"],[0.75,0.25,0],[80,100,70,50,50,45]),
"MACHAMP" : Template(68,"Machamp",["FIGHTING"],[0.75,0.25,0],[90,130,80,65,65,55]),
"BELLSPROUT" : Template(69,"Bellsprout",["GRASS","POISON"],[0.5,0.5,0],[50,75,35,70,70,40]),
"WEEPINBELL" : Template(70,"Weepinbell",["GRASS","POISON"],[0.5,0.5,0],[65,90,50,85,85,55]),
"VICTREEBEL" : Template(71,"Victreebel",["GRASS","POISON"],[0.5,0.5,0],[80,105,65,100,100,70]),
"TENTACOOL" : Template(72,"Tentacool",["WATER","POISON"],[0.5,0.5,0],[40,40,35,100,100,70]),
"TENTACRUEL" : Template(73,"Tentacruel",["WATER","POISON"],[0.5,0.5,0],[80,70,65,120,120,100]),
"GEODUDE" : Template(74,"Geodude",["ROCK","GROUND"],[0.5,0.5,0],[40,80,100,30,30,20]),
"GRAVELER" : Template(75,"Graveler",["ROCK","GROUND"],[0.5,0.5,0],[55,95,115,45,45,35]),
"GOLEM" : Template(76,"Golem",["ROCK","GROUND"],[0.5,0.5,0],[80,110,130,55,55,45]),
"PONYTA" : Template(77,"Ponyta",["FIRE"],[0.5,0.5,0],[50,85,55,65,65,90]),
"RAPIDASH" : Template(78,"Rapidash",["FIRE"],[0.5,0.5,0],[65,100,70,80,80,105]),
"SLOWPOKE" : Template(79,"Slowpoke",["WATER","PSYCHIC"],[0.5,0.5,0],[90,65,65,40,40,15]),
"SLOWBRO" : Template(80,"Slowbro",["WATER","PSYCHIC"],[0.5,0.5,0],[95,75,110,80,80,30]),
"MAGNEMITE" : Template(81,"Magnemite",["ELECTRIC"],[0,0,1],[25,35,70,95,95,45]),
"MAGNETON" : Template(82,"Magneton",["ELECTRIC"],[0,0,1],[50,60,95,120,120,70]),
"FARFETCHD" : Template(83,"Farfetch'd",["NORMAL","FLYING"],[0.5,0.5,0],[52,65,55,58,58,60]),
"DODUO" : Template(84,"Doduo",["NORMAL","FLYING"],[0.5,0.5,0],[35,85,45,35,35,75]),
"DODRIO" : Template(85,"Dodrio",["NORMAL","FLYING"],[0.5,0.5,0],[60,110,70,60,60,100]),
"SEEL" : Template(86,"Seel",["WATER"],[0.5,0.5,0],[65,45,55,70,70,45]),
"DEWGONG" : Template(87,"Dewgong",["WATER","ICE"],[0.5,0.5,0],[90,70,80,95,95,70]),
"GRIMER" : Template(88,"Grimer",["POISON"],[0.5,0.5,0],[80,80,50,40,40,25]),
"MUK" : Template(89,"Muk",["POISON"],[0.5,0.5,0],[105,105,75,65,65,50]),
"SHELLDER" : Template(90,"Shellder",["WATER"],[0.5,0.5,0],[30,65,100,45,45,40]),
"CLOYSTER" : Template(91,"Cloyster",["WATER","ICE"],[0.5,0.5,0],[50,95,180,85,85,70]),
"GASTLY" : Template(92,"Gastly",["GHOST","POISON"],[0.5,0.5,0],[30,35,30,100,100,80]),
"HAUNTER" : Template(93,"Haunter",["GHOST","POISON"],[0.5,0.5,0],[45,50,45,115,115,95]),
"GENGAR" : Template(94,"Gengar",["GHOST","POISON"],[0.5,0.5,0],[60,65,60,130,130,110]),
"ONIX" : Template(95,"Onix",["ROCK","GROUND"],[0.5,0.5,0],[35,45,160,30,30,70]),
"DROWZEE" : Template(96,"Drowzee",["PSYCHIC"],[0.5,0.5,0],[60,48,45,90,90,42]),
"HYPNO" : Template(97,"Hypno",["PSYCHIC"],[0.5,0.5,0],[85,73,70,115,115,67]),
"KRABBY" : Template(98,"Krabby",["WATER"],[0.5,0.5,0],[30,105,90,25,25,50]),
"KINGLER" : Template(99,"Kingler",["WATER"],[0.5,0.5,0],[55,130,115,50,50,75]),
"VOLTORB" : Template(100,"Voltorb",["ELECTRIC"],[0,0,1],[40,30,50,55,55,100]),
"ELECTRODE" : Template(101,"Electrode",["ELECTRIC"],[0,0,1],[60,50,70,80,80,140]),
"EXEGGCUTE" : Template(102,"Exeggcute",["GRASS","PSYCHIC"],[0.5,0.5,0],[60,40,80,60,60,40]),
"EXEGGUTOR" : Template(103,"Exeggutor",["GRASS","PSYCHIC"],[0.5,0.5,0],[95,95,85,125,125,55]),
"CUBONE" : Template(104,"Cubone",["GROUND"],[0.5,0.5,0],[50,50,95,40,40,35]),
"MAROWAK" : Template(105,"Marowak",["GROUND"],[0.5,0.5,0],[60,80,110,50,50,45]),
"HITMONLEE" : Template(106,"Hitmonlee",["FIGHTING"],[1,0,0],[50,120,53,35,35,87]),
"HITMONCHAN" : Template(107,"Hitmonchan",["FIGHTING"],[1,0,0],[50,105,79,35,35,76]),
"LICKITUNG" : Template(108,"Lickitung",["NORMAL"],[0.5,0.5,0],[90,55,75,60,60,30]),
"KOFFING" : Template(109,"Koffing",["POISON"],[0.5,0.5,0],[40,65,95,60,60,35]),
"WEEZING" : Template(110,"Weezing",["POISON"],[0.5,0.5,0],[65,90,120,85,85,60]),
"RHYHORN" : Template(111,"Rhyhorn",["GROUND","ROCK"],[0.5,0.5,0],[80,85,95,30,30,25]),
"RHYDON" : Template(112,"Rhydon",["GROUND","ROCK"],[0.5,0.5,0],[105,130,120,45,45,40]),
"CHANSEY" : Template(113,"Chansey",["NORMAL"],[0,1,0],[250,5,5,105,105,50]),
"TANGELA" : Template(114,"Tangela",["GRASS"],[0.5,0.5,0],[65,55,115,100,100,60]),
"KANGASKHAN" : Template(115,"Kangaskhan",["NORMAL"],[0,1,0],[105,95,80,40,40,90]),
"HORSEA" : Template(116,"Horsea",["WATER"],[0.5,0.5,0],[30,40,70,70,70,60]),
"SEADRA" : Template(117,"Seadra",["WATER"],[0.5,0.5,0],[55,65,95,95,95,85]),
"GOLDEEN" : Template(118,"Goldeen",["WATER"],[0.5,0.5,0],[45,67,60,50,50,63]),
"SEAKING" : Template(119,"Seaking",["WATER"],[0.5,0.5,0],[80,92,65,80,80,68]),
"STARYU" : Template(120,"Staryu",["WATER"],[0,0,1],[30,45,55,70,70,85]),
"STARMIE" : Template(121,"Starmie",["WATER","PSYCHIC"],[0,0,1],[60,75,85,100,100,115]),
"MRMIME" : Template(122,"Mr. Mime",["PSYCHIC"],[0.5,0.5,0],[40,45,65,100,100,90]),
"SCYTHER" : Template(123,"Scyther",["BUG","FLYING"],[0.5,0.5,0],[70,110,80,55,55,105]),
"JYNX" : Template(124,"Jynx",["ICE","PSYCHIC"],[0,1,0],[65,50,35,95,95,95]),
"ELECTABUZZ" : Template(125,"Electabuzz",["ELECTRIC"],[0.75,0.25,0],[65,83,57,85,85,105]),
"MAGMAR" : Template(126,"Magmar",["FIRE"],[0.75,0.25,0],[65,95,57,85,85,93]),
"PINSIR" : Template(127,"Pinsir",["BUG"],[0.5,0.5,0],[65,125,100,55,55,85]),
"TAUROS" : Template(128,"Tauros",["NORMAL"],[1,0,0],[75,100,95,70,70,110]),
"MAGIKARP" : Template(129,"Magikarp",["WATER"],[0.5,0.5,0],[20,10,55,20,20,80]),
"GYARADOS" : Template(130,"Gyarados",["WATER","FLYING"],[0.5,0.5,0],[95,125,79,100,100,81]),
"LAPRAS" : Template(131,"Lapras",["WATER","ICE"],[0.5,0.5,0],[130,85,80,95,95,60]),
"DITTO" : Template(132,"Ditto",["NORMAL"],[0,0,1],[48,48,48,48,48,48]),
"EEVEE" : Template(133,"Eevee",["NORMAL"],[0.875,0.125,0],[55,55,50,65,65,55]),
"VAPOREON" : Template(134,"Vaporeon",["WATER"],[0.875,0.125,0],[130,65,60,110,110,65]),
"JOLTEON" : Template(135,"Jolteon",["ELECTRIC"],[0.875,0.125,0],[65,65,60,110,110,130]),
"FLAREON" : Template(136,"Flareon",["FIRE"],[0.875,0.125,0],[65,130,60,110,110,65]),
"PORYGON" : Template(137,"Porygon",["NORMAL"],[0,0,1],[65,60,70,75,75,40]),
"OMANYTE" : Template(138,"Omanyte",["ROCK","WATER"],[0.875,0.125,0],[35,40,100,90,90,35]),
"OMASTAR" : Template(139,"Omastar",["ROCK","WATER"],[0.875,0.125,0],[70,60,125,115,115,55]),
"KABUTO" : Template(140,"Kabuto",["ROCK","WATER"],[0.875,0.125,0],[30,80,90,45,45,55]),
"KABUTOPS" : Template(141,"Kabutops",["ROCK","WATER"],[0.875,0.125,0],[60,115,105,70,70,80]),
"AERODACTYL" : Template(142,"Aerodactyl",["ROCK","FLYING"],[0.875,0.125,0],[80,105,65,60,60,130]),
"SNORLAX" : Template(143,"Snorlax",["NORMAL"],[0.875,0.125,0],[160,110,65,65,65,30]),
"ARTICUNO" : Template(144,"Articuno",["ICE","FLYING"],[0,0,1],[90,85,100,125,125,85]),
"ZAPDOS" : Template(145,"Zapdos",["ELECTRIC","FLYING"],[0,0,1],[90,90,85,125,125,100]),
"MOLTRES" : Template(146,"Moltres",["FIRE","FLYING"],[0,0,1],[90,100,90,125,125,90]),
"DRATINI" : Template(147,"Dratini",["DRAGON"],[0.5,0.5,0],[41,64,45,50,50,50]),
"DRAGONAIR" : Template(148,"Dragonair",["DRAGON"],[0.5,0.5,0],[61,84,65,70,70,70]),
"DRAGONITE" : Template(149,"Dragonite",["DRAGON","FLYING"],[0.5,0.5,0],[91,134,95,100,100,80]),
"MEWTWO" : Template(150,"Mewtwo",["PSYCHIC"],[0,0,1],[106,110,90,154,154,130]),
"MEW" : Template(151,"Mew",["PSYCHIC"],[0,0,1],[100,100,100,100,100,100]),
}