from asyncore import write
from queue import Empty
import urllib.request, json 
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
			'AppleWebKit/537.11 (KHTML, like Gecko) '
			'Chrome/23.0.1271.64 Safari/537.11',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'en-US,en;q=0.8',
			'Connection': 'keep-alive'}
url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?&startdate=03/08/2002&enddate=12/31/2007&dateregion=tcg_date"
request = urllib.request.Request(url, None, header)

#list of cards that are forbidden/limited according to the September 2007 TCG Banlist (see: https://yugipedia.com/wiki/September_2007_Lists_(TCG))
#0
perfectCircleBannedCards = [
	504700118]

#1
perfectCircleLimitedCards = [
	71413901]

#2
perfectCircleSemiLimitedCards = [
	504700013]

#-1
perfectCircleIllegalCards = [
	511006006,511003018,511003026,511006005,511006010,511003021,511000566,511000572,513000053,
	511020012,511002048,513000001,511000559,511002613,511000574,511002616,160403001,511002614,
	511009557,511000567,511002049,511001128,160001015,511003075,511009564,511000568,511002513,
	511003056,511019009,511019001,511600239,511019002,511019003,160001012,511009331,511002828,
	160001002,511001595,160001010,160001001,160001008,160001009,513000030,511002418,513000028,
	513000029,513000095,511000378,511002501,511004006,511000695,511000769,511002506,511002507,
	511002508,511000539,511600061,511000565,511600100,511600166,810000114,511001147,511000560,
	511000570,511002504,511000562,511010701,511004015,511015127,511002127,511600189,511310000,
	511000575,810000028,513000142,511005647,511000573,511000569,511002167,511000564,511009014,
	511600169,511756001,511600069,511002500,511600193,511000772,511001040,160404002,511000563,
	511002854,511018019,511000590,511000462,511001057,511018028,511000477,511002533,511000571,
	511000591,511000240,160001040,160001042,160001043,160404003,511000218,511000474,511000548,
	511001126,511001651,511002057,511002295,511002403,511002415,511002531,511002540,511002549,
	511002825,511008009,511018004,511021008,511600096,511600170,511777003,511777009,513000054,
	513000055,513000116,511000241,511000373,511000377,511000541,511000604,511002523,511002539,
	511004341,511005063,511600004,511600290,511000258,511002461,511002578,511004007,511010700,
	511002499,810000042,810000043,160001045,160001048,511000278,511000475,511000987,511001122,
	511002446,511002884,511005091,511020009,511600062,810000055,511000248,511001016,511001887,
	511002444,513000002,513000026,513000066,513000111,511013024,511003023,511000540,511310007,
	26534688,74335036,34103656,2819435,160406009,160003011,160406001,160406002,160003010,
	160001011,160003008,160002004,160003007,160003006,160003005,160002014,160406006,160002040,
	160002041,160002044,160201011,160406010,160003052,160003053,160002050,44508094
]

#This is a temporary fix until YGOPRODECK includes portuguese commons for OP15, OP16 and OP17 specifically
portugueseOTSLegalCards = [
	98259197,40391316,24040093,98024118,19439119,10118318,47395382,29905795,66976526,60470713,
	76442347,36318200,15941690,88552992,4192696,2461031,16550875,69207766,90576781,21179143,
	64514622,3300267,31516413,78033100,41639001,13140300,8611007,51555725,38492752,32761286]

#(C) is common, (SP) is Short Print, (SSP) is Super Short Print, (DNPR) is Duel Terminal common
legalRarities = ['(C)', '(SP)', '(SSP)', '(DNPR)']

#Banlist status
banned = 'Banned'
limited = 'Limited'
semi = 'Semi-Limited'

#YGOPRODECK API keys
data = 'data'
card_sets = 'card_sets'
banlist_info = 'banlist_info'
ban_tcg = 'ban_tcg'
rarity_code = 'set_rarity_code'
card_images = 'card_images'
cardType = 'type'

#Token stuff
token = 'Token'

#My keys
name = 'name'
cardId = 'id'
status = 'status'

#Filename for banlist
filename = 'PerfectCircle.lflist.conf'

#def writeCard(card, outfile):
#	outfile.write("%d %d -- %s\n" % (card.get(cardId), card.get(status), card.get(name)))

def writeCardWithoutDB(id, status, outfile):
	outfile.write("%d %s\n" % (id, status))

#Go to the DB and get the ID of every single card
with urllib.request.urlopen(request) as url:
	cards = json.loads(url.read().decode()).get(data)
	legalCards = []
	simpleCards = []
	ocgCards = []
	for card in cards:
		if card.get(card_sets) != None:
			images = card.get(card_images)
			for variant in images:
				legalCards.append(variant.get(cardId))
			banInfo = card.get(banlist_info)
			banTcg = 3
			if (banInfo == None):
				banTcg = 3	
			if (banInfo != None):
				banlistStatus = banInfo.get(ban_tcg)
				if (banlistStatus == None):
					banTcg = 3
				if (banlistStatus == banned):
					banTcg = 0
				if (banlistStatus == limited):
					banTcg = 1
				if (banlistStatus == semi):
					banTcg = 2
			cardSets = card.get(card_sets)
			hasCommonPrint = False
			for printing in cardSets:
				if printing.get(rarity_code) in legalRarities:
					hasCommonPrint = True

			#Portuguese fix, remove as soon as YGOPRODECK adds portuguese OTS support
			if not hasCommonPrint:
				if card.get(cardId) in portugueseOTSLegalCards:
					hasCommonPrint = True

			if not hasCommonPrint:
				banTcg = -1

			if (banTcg<3):
				for variant in images:
					simpleCard = {}
					simpleCard[name] = card.get(name)
					simpleCard[status] = banTcg
					simpleCard[cardId] = variant.get(cardId)
					simpleCards.append(simpleCard)
		if (card.get(card_sets)) == None and card.get(cardType) != token:
			simpleCard = {}
			simpleCard[name] = card.get(name)
			simpleCard[status] = -1
			for variant in card.get(card_images):
				simpleCard[cardId] = variant.get(cardId)
				ocgCards.append(simpleCard)
	with open(filename, 'w', encoding="utf-8") as outfile:
		outfile.write("#[2007.9 TCG]\n")
		outfile.write("!2007.9 TCG\n")
		outfile.write("$whitelist\n")
		outfile.write("#Banned\n")
		for id in perfectCircleBannedCards:
			writeCardWithoutDB(id, 0, outfile)
		outfile.write("#Limited\n")
		for id in perfectCircleLimitedCards:
			writeCardWithoutDB(id, 1, outfile)
		outfile.write("#Semi-Limited\n")
		for id in perfectCircleSemiLimitedCards:
			writeCardWithoutDB(id, 2, outfile)
		outfile.write("#Unlimited List\n")
		#print(legalCards[0]);
		for id in legalCards:
			writeCardWithoutDB(id, 3, outfile)
		outfile.write("#Illegal Cards\n")
		for id in perfectCircleIllegalCards:
			writeCardWithoutDB(id, -1, outfile)
		#for card in ocgCards:
		#	writeCard(card, outfile)
		#outfile.write("\n#Regular Banlist\n\n")
		#for card in simpleCards:
		#	writeCard(card, outfile)