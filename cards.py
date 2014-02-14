class Base(object):
	required = []
	optional = []
	def __init__(self, json_data):
		for attr in self.required:
			setattr(self, attr, json_data[attr])
		for attr, default in self.optional.items():
			setattr(self, attr, json_data[attr] if attr in json_data else default)

class Edition(Base):
	required = ["set","layout","artist","url","number","rarity","multiverse_id","image_url","set_url"]
	optional = {
		"flavor": 		"",
		"watermark": 	"",
        "price":        {"low":0, "average":0, "high":0}
	}
	def __init__(self, card, json_data):
		super(Edition, self).__init__(json_data)
		self.card = card
        self.price.pop("note",None)
		# self.price_low = json_data["price"]["low"]
		# self.price_average = json_data["price"]["average"]
		# self.price_high = json_data["price"]["high"]
	def __repr__(self):
		return "<Card: %s (%s)>"%(self.card.name, self.set)
	__unicode__ = __repr__


class Card(Base):
	required = ["id","name","url","text","types","cmc","cost","formats"]
	optional = {
		"colors":		[],
		"subtypes":		[],
		"supertypes":	[],
		"power":		-1,
		"toughness":	-1,
		"loyalty":		-1,
	}
	def __init__(self, json_data):
		super(Card, self).__init__(json_data)
		
		self.editions = [Edition(self, ed) for ed in json_data["editions"]]
	def __repr__(self):
		return "<Card: %s>"%(self.name)
	__unicode__ = __repr__