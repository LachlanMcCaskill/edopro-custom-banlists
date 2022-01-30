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
	504700118,9596126,511000819,34124316,69015963,78706415]

#1
perfectCircleLimitedCards = [
	71413901]

#2
perfectCircleSemiLimitedCards = [
	504700013]

#-1
perfectCircleIllegalCards = [
	511003222,511003217,511003218,511003211,511027027,511027455,511600382,511600383,511600384,511600385,511600386,511600374,511600373,511001439,511002592,511001808,511001895,511015125,513000157,513000124,511600141,513000128,513000019,513000127,513000088,513000092,511030047,511018016,513000090,513000108,511003204,513000115,511002635,511600241,513000082,513000084,513000103,513000037,513000125,513000149,513000158,513000146,513000150,513000148,513000159,511600294,513000153,513000152,513000155,513000154,513000156,513000147,513000145,513000184,511010536,513000140,513000132,513000178,513000165,513000185,513000163,513000126,513000099,513000172,511600422,511600421,511600420,511600419,511600413,513000177,511600412,513000176,511600411,513000175,511600410,513000174,513000166,511600405,513000171,511600404,513000170,511600403,513000169,511600402,513000168,511600406,511600407,511600408,511600416,511600414,511600417,511600415,511600423,513000025,513000097,511050013,511018007,511050012,511002532,700000014,511002547,511002616,511000308,511013020,511003021,511002728,511003056,150000091,511023004,511002072,511013016,511001976,810000029,511001742,511002267,511000078,511009951,511016003,511002507,810000097,511002895,511001049,511002239,511002894,511000604,511005642,511009322,513000014,511000307,513000096,511001516,511024008,511247004,513000013,511000368,511600299,511002911,511002009,513000121,511002048,511002641,511010173,511003019,511009522,511002869,511000662,100000510,511009349,100000410,511600056,511002846,511002983,511009443,511002013,511015134,511004015,511009387,511000133,511600067,513000024,511009001,100000150,513000004,511015133,511002946,511000987,511600127,511000587,511247011,511027018,511000475,511023001,511002426,511600099,511013001,511600279,511600293,511009917,151000033,100000001,513000087,100000155,511000997,511018022,511001723,511010103,100000244,513000066,511600267,511018009,511030013,511018030,511005709,511002864,511003205,511009376,511009683,513000062,511106005,511000264,511020009,511001967,511000293,511002835,511002188,511002702,511001025,511002873,511000373,511002751,511009022,511002370,511002278,511002826,100000009,513000041,511600377,511030036,511002625,511000421,810000077,100000006,513000040,511000012,511001074,511000695,511600369,511009077,100000502,511001943,511600268,511600287,511001952,511002617,511007019,511009331,511002581,511009053,511001282,511002838,511001782,511010035,511001942,511009095,511000772,511003068,511000765,511002988,511003069,511756009,511001700,511002760,511003029,513000179,511013017,511001658,511013014,170000201,511600012,511000788,511023014,511001989,100000365,511001712,700000000,511005091,511030014,511002855,511600174,511000362,513000095,511002552,700000015,511002623,511010508,511000670,511777005,511010107,511001999,511001136,511001939,513000030,100000069,513000106,511010239,511002549,511600096,511002500,511002628,100000296,511002483,511001616,511001109,511002477,151000016,511002862,700000018,511310011,511001956,511050003,511009307,511005715,511003005,511027101,511009088,511600203,511002223,511600007,511002543,511009627,511600023,700000020,511000415,513000180,511002001,511019007,151000044,513000107,511009564,511009340,511002079,511010511,511002768,700000010,511002841,511027091,511000613,170000203,511106011,511600364,151000005,511000378,511002018,511000763,511009705,511600357,511002872,511002377,511002487,511030062,511013011,511009537,511001291,511002675,170000154,511009593,170000204,511002059,511027117,100000412,511001744,111302501,511010702,511002076,511010039,511600272,511002599,511001957,511000614,810000109,170000194,511001628,511001795,100000511,511015100,511002136,511310001,511018029,511002374,511600286,511000754,151000050,100000512,511600348,511013031,511600199,511247015,511010007,511001663,511600352,511003045,170000170,511024000,511002034,511002513,511010502,511020000,511002402,511001695,511002888,511000372,511000769,511027106,511001056,100000093,513000098,511010030,511017001,511005063,511002039,511002665,511009162,511002200,511247012,511001949,151000028,511756002,511600082,511002228,810000055,100000247,513000057,511600361,511002083,511001997,511000532,511009051,511001693,511003023,511003066,511001010,511600376,810000102,511009369,511001501,100000315,511002480,511002883,511000169,100000411,511600062,511003028,511010011,810000006,170000202,810000011,511000430,100000126,511016004,810000096,511600140,511006006,511000212,511027120,511000263,511310014,511000277,511002976,511001784,511000915,511009543,511001139,511002463,511600253,511009180,511600121,511001702,511600304,511002514,511000232,511005646,511000431,511023006,511004438,511030039,511001391,511009071,511009950,511009126,511030044,511002125,151000010,511002737,511001146,511018024,513000053,513000094,511013023,511600064,511002706,511001050,511600314,511000276,511004443,511013022,810000045,511002518,100003002,511009558,511010196,700000001,511030043,511002880,511002499,511002467,511002877,511009194,511010507,511001785,511016005,511014001,511001964,511009065,100000100,513000104,511002195,511600042,511001521,511002749,511015127,511002990,511001121,511002764,151000022,511002528,511002836,511023000,511000208,511002830,170000158,511030006,511000462,511008010,511015129,511021010,511025000,511000623,511003027,511002319,511001651,511002652,511023013,511001043,513000039,511002601,513000072,511002057,511002839,511003004,511000300,511600091,511000541,511247005,511002046,511600290,511000674,511005008,511009393,511002040,511009364,511001415,511009704,511015117,511002775,511005633,511009047,511002031,100000014,513000051,511002219,100000159,700000011,511001116,100001010,511009389,511001279,511010514,511002808,511001769,511013000,511001454,513000144,100000526,511002574,511002002,511247002,511310013,100000113,511600083,511002096,511014000,511002403,511001565,513000038,511600050,511004436,100000488,511247001,511010513,511000064,511600139,511002879,511600033,511002771,511001253,511009517,511000639,500314701,511009542,511000410,511023012,511001252,511600381,100000104,511000165,511002952,511002545,810000103,511000262,511000261,100000482,511005639,511010205,511002077,511009442,511002359,511002589,511600353,511600125,511600126,511018017,511001371,511002610,511010503,511015132,511009706,511002353,511002263,511000592,511002807,511006005,511002963,511010207,511002761,100000050,511600401,513000167,511002203,100000129,511003087,513000054,100000122,511001363,100000151,511600039,511600260,100000110,513000162,511009000,511002598,511002515,511600171,511009918,511001429,511002821,511015114,511000260,513000078,511002670,511010238,511600201,100000153,513000186,100000537,511002505,100000243,511000183,511050008,511003025,511050002,511030045,511004407,511001721,511001944,513000026,511002772,100000532,511010032,511002981,511019002,511001986,511002863,810000078,511000036,513000091,511002265,511002816,100000015,513000044,511000192,511001595,511010537,511600119,511000420,150000077,511000072,513000182,513000035,511001517,511001594,100000355,511002108,511010025,511019003,511009072,511003060,810000022,511009064,511002759,511000013,511013033,511247007,511009086,511001052,511001202,511002489,511001275,511002111,511003057,511009308,511600073,511002517,100000154,511600137,511003067,511600170,100000275,511002101,511000477,511600021,511002379,511600092,511001910,511009380,511002485,511016002,511600251,511002859,511011004,511001051,511001069,511009342,511310010,511001973,511000513,511000279,511021009,511002508,151000015,511001603,151000051,513000137,511600118,511600305,511003081,511002913,511756003,511001122,511009425,511010535,511003062,511600298,511002896,100000505,511002746,511002533,100000282,511000760,511009191,511001060,450000001,511600378,511009305,511009110,511009416,511600266,511002762,511002288,511006003,511002382,511013007,511310113,511600322,511600106,100000004,513000050,511000743,511600355,700000009,511001149,511003089,511002774,511002222,511010105,511600197,511000286,100000025,511600306,511001369,511002109,151000057,511009952,511009540,511002709,511600295,511002080,511001743,511000515,100000265,511002882,511002776,511002850,511001459,170000155,511106012,511002520,511009588,511002213,511015116,511000258,513000139,513000008,513000009,511010021,511001786,511030005,511050004,170000149,100000501,511013018,511600051,511002757,511000369,511001724,511000749,511018019,511003202,511013009,511010139,511001706,511001186,151000018,511016006,511002738,511002910,511600048,151000029,511001776,511600068,511600124,511009351,511010056,511001431,511006010,511756001,511600351,511002587,511010096,511002777,511002277,511003115,511027000,511007001,511013021,511001924,513000069,511002446,511001514,511023010,511001779,511030068,511002689,511003064,511001945,511600359,513000018,513000122,511600263,511000552,511002650,511002727,511001247,151000052,100000508,511001692,511002884,100000257,511001941,511050011,511003063,511600001,511000512,511310007,511001887,810000051,511600362,511002042,511002418,170000210,511002856,511012000,511001950,511600215,511600070,511002444,511001601,511002371,513000111,100001001,511001624,700000012,511023002,511002915,511005647,511001732,511002021,511002049,511001625,700000028,511001289,511002060,511000118,511001974,511009381,513000061,511000377,511600204,511000076,513000015,511002861,513000022,513000029,511009066,511001766,511130000,511600176,511027121,810000050,511002741,700000016,511003047,511010701,511002544,511001211,151000030,511756000,511002773,511001653,511600379,511009016,511777001,511024010,511600061,511023015,511009013,511009068,511001963,511600109,511001040,511600166,810000114,511000923,511009583,511009368,511002870,511002214,511600004,511002871,511003065,511002229,511023007,511000024,513000089,511010132,511777008,511010165,511002372,511009026,511009062,511010703,511002600,511002813,511002309,511010083,511002597,511002419,513000017,511600274,511002166,511009193,511001290,511030008,511003010,511009104,511002710,511010020,511004111,511002375,511001822,511106008,511777006,511001542,511001374,511600370,511002876,511001129,511010192,511600080,511002542,511017002,511001661,511018001,511002045,511001212,511018012,170000197,511000434,511000255,170000153,511015112,511001868,511003000,111011901,511001770,151000040,511003203,511009073,511027093,511001791,511002003,100000529,511002858,511600052,511002906,511002716,511021003,511005043,511030007,511001128,511001405,511027103,511001419,511002227,511009587,511001489,511005712,511015108,100000094,344000000,511024005,511001160,511017003,100000167,511002490,511009545,511600335,513000001,511010534,170000157,511600252,511000164,511002951,810000098,511002546,100000020,511000429,511002590,511310017,511000737,511002531,511001699,511009528,511001014,511000253,511015124,100000545,511247017,511600122,100005002,513000161,511001251,511003039,511009567,511001539,511009061,511002521,511002756,511003080,511001126,511003059,511009311,511020001,511001622,511600310,511001701,511015110,511000231,511009508,511020002,511001789,511003058,511024011,511001416,511030055,511002526,511003090,511023005,511005006,511000539,511002194,511002673,511000275,513000164,511600284,511600311,511009651,511001124,511009025,511010505,511000252,511019006,511024007,511000480,511004437,511001396,511001278,511002358,511600014,511027104,511023011,511000251,511004126,810000034,511002796,511002854,511009165,511806001,511013005,511002486,100000478,511001117,511004441,511002755,810000052,511009412,511600069,100000086,511002036,511002828,511010064,511001981,511002739,100000336,511600013,511013028,511002530,100003003,511019009,511002276,511027111,511002035,100000527,810000075,511000168,511003074,511002091,511000657,511002273,511009480,511010704,511000419,511001644,511013026,511018002,511002416,100000318,511600100,511600105,511002642,511001780,511002624,511013035,511021006,151000020,511000278,511001983,511001593,513000036,511001273,511600182,511001455,511002350,513000076,511600313,511756006,511008508,511003073,100000013,513000047,511001637,511050010,511016001,511000073,513000183,511600027,513000075,511013029,511001055,511018013,511009313,511600026,511002539,511009323,511009386,511002092,511600005,511600006,511005042,511003208,151000001,513000031,511013032,511018028,513000120,511030004,511008009,150000085,511009385,511009424,511009527,511600380,511806000,511000761,511004444,511005701,110000102,511310005,511003070,511002945,511002957,511002295,810000105,511002818,511002827,511016000,511001245,511009192,511000070,511002155,511021000,511002221,511001992,511310012,511600049,511008509,100000003,513000042,511001771,511000474,511002612,511600318,511000306,511600110,511002012,511002482,511018000,511021008,511000366,511002831,511010500,511310003,511000250,511009365,511027135,511001426,511000241,511001954,511002381,511002286,511002504,511001425,151000019,100000002,513000049,511009142,100000536,511002260,511001823,511005066,513000079,511009109,511001659,511000246,511005034,511001777,151000041,511013004,100000125,511000589,511001041,511002274,511247013,511010034,511005737,511002969,511001395,100000056,511600409,513000173,100000156,511600138,511002611,511004006,511010062,511600424,513000142,100000128,100000121,511002064,511002615,511010047,511002676,511600280,511001645,511009055,511030042,511005637,511009304,511001703,511001274,511002829,511010700,511000247,511600212,511600367,100000533,100000245,511001926,511001522,810000111,511106004,511013025,511000821,513000016,511002088,810000028,511023008,511027102,511310019,511002484,511777003,511002865,511001710,511001147,511310009,511247003,511247009,100000007,513000003,511020004,511013010,511003018,511004004,511600038,511600194,511001946,511002664,511600262,151000007,511009041,511002502,100000509,511600020,511001947,511001597,511003072,100001007,100001006,810000057,100000010,513000048,511000799,511001632,511001433,511600269,100000274,511009214,511010531,511106009,511001704,511030022,511019001,511001948,511009353,511002387,511002509,511000774,511001821,511027094,511013003,511002506,511600181,511002954,511002415,511002614,810000019,700000013,511000503,511009350,511001284,100000483,511002470,511000000,511010532,511001951,511000558,511015120,511000364,511000077,700000017,511600301,511001596,511600104,511009954,511777007,513000012,700000029,511002848,511010530,511002373,511001283,100000304,511002578,511001975,511003088,511130002,513000055,511002825,511010053,511006007,511009955,700000019,511030003,700000027,511027024,511002793,511002989,151000053,511000806,511001711,511005644,511002540,511001608,511002268,511600308,100000507,100000152,170000150,511247010,511600128,151000025,511002184,151000026,151000049,511015115,511009043,511009735,511009018,511018004,511003071,513000002,511009628,511009444,511000309,511600366,511247008,511010501,513000116,511009002,511001725,511004423,511002461,511002878,511000248,513000060,511002524,511000807,511000184,511002651,513000138,511600235,100000075,100000258,511002984,511027110,511002860,100000111,511021005,511001430,511001567,511009916,511002519,513000063,511000995,511018021,511010538,511001445,511021004,511009684,511020011,100000530,513000056,511001966,511009059,511000548,511001404,170000193,511310038,511005711,511015126,511003003,511010012,511013024,513000021,511002050,511002037,511010504,511010515,511001057,511002794,511247020,511001016,511600117,344000001,511000508,100000542,511002960,100000091,513000071,511002541,511002452,151000031,100000506,511600081,511231002,511000302,511009553,511600103,511027025,511000642,511600169,511021001,511001873,511001962,511600115,511009170,100000471,511600291,100000042,511001698,511002729,511001646,500000051,511001652,511002591,511310000,511001277,511600003,511001694,511002476,511001435,511000119,511001713,511600076,511000218,511000149,511777010,511600090,511002352,511002534,100000302,511002982,511000675,511012001,511009049,511002958,511002525,511001955,511001696,511002488,511600296,511009530,511005645,511001376,511600302,511003026,140000074,511002844,511004447,511310016,511050007,100000199,511600130,511005643,511002135,511004007,511000230,511000242,511009462,100000301,511009014,513000028,511002126,511001403,511001961,511021002,511002953,511000432,511002750,511002293,511002261,511002523,511004341,511001778,511010533,511600315,511002501,511000627,151000027,511003022,511015121,511002127,511600189,511000243,511019008,511013002,100000087,511777009,511130001,511002708,511000599,511002849,511009441,100000084,511002912,511600342,511002378,511002834,511003075,511600108,810000002,513000059,511009136,511000240,511002845,100000531,511009321,511002814,810000026,511600300,511001044,511002866,511001599,511001286,511010010,511600133,511002220,511001108,170000151,511002659,140000131,511756008,511000239,511310015,511009572,513000011,511009685,511003207,511600347,511002054,810000110,511018014,511001600,511002991,511002044,511018015,151000024,511002874,110000012,513000136,110000010,513000134,110000011,513000135,511002081,511106010,511310002,810000071,511000433,511004442,511013027,513000068,511020007,100000012,513000046,511013015,511002351,100000073,511002090,511030023,511002726,511247000,511027112,511009413,513000052,100001009,511600047,511004440,511001993,511002718,511600193,511600271,511002425,511600120,511024006,513000074,511009384,100100090,511002110,511003077,100000008,513000045,511002380,810000031,170000167,151000021,511001564,511600239,511600025,511002011,511011003,511010506,511002058,511009406,511600387,511001417,100000233,511000549,511002909,511009544,511009531,100000005,513000043,511001783,511010519,511001965,511009569,511002740,511024001,511001781,511009557,513000083,100000124,511002961,511001372,810000106,511000234,511002810,511002857,511003201,511000629,511002603,511600129,511009635,511002833,511600254,511001697,511002613,100000127,511015128,511000497,511001432,511004439,810000081,511002837,511015111,511001392,511030056,511002962,151000056,100000061,511600418,511024009,511024002,151000043,511002202,810000056,511002527,100000120,511002602,151000058,511000233,100000303,511002959,511030054,511050001,511002112,511010065,511009300,511004434,511247006,511010525,511002464,511310008,100003004,511018010,511600205,511030061,511001982,511247018,511007022,511009054,511002732,511247014,100000534,511001123,511001998,511020012,511020010,511027107,511600077,511000902,513000141,511600116,511756007,511002985,100000538,511002763,511001598,511002529,151000054,511010104,511020008,511010009,511020005,511002824,511310006,170000152,513000070,511000817,511009074,511002809,511015118,511002321,511000074,511009919,511000376,511247019,511002701,511001639,511013008,511001048,511009089,511000436,511001409,511003206,151000003,513000073,511000770,511002075,810000017,511777004,810000042,810000043,511000075,513000181,511600022,100000280,511002881,511025002,511020003,511000540,511009402,511002167,511009091,160001000,160001001,160001002,160001004,160001006,160001007,160001008,160001009,160001010,160001011,160001012,160001013,160001014,160001015,160001040,160001042,160001043,160001045,160001047,160001048,160002000,160002004,160002005,160002014,160002015,160002040,160002041,160002044,160002050,160003000,160003004,160003005,160003006,160003007,160003008,160003009,160003010,160003011,160003052,160003053,160004000,160201009,160201011,160202004,160202019,160202048,160401002,160403001,160404001,160404002,160404003,160406001,160406002,160406006,160406007,160406008,160406009,160406010,160407001,74335036,2819435,26534688,34103656,75402014,160412010,160006010,160203012,160412009,160204042,160405008,160412008,160004011,160406007,160003004,160412006,160411002,160204041,160204040,160304022,160005054,160203015,160001047,
	#Cards with Errata
	72989439,82301904
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
		outfile.write("#[2007.9 Perfect Circle (TCG)]\n")
		outfile.write("!2007.9 Perfect Circle (TCG)\n")
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
			if(id not in perfectCircleBannedCards):
				writeCardWithoutDB(id, 3, outfile)
		outfile.write("#Illegal Cards\n")
		for id in perfectCircleIllegalCards:
			writeCardWithoutDB(id, -1, outfile)
		#for card in ocgCards:
		#	writeCard(card, outfile)
		#outfile.write("\n#Regular Banlist\n\n")
		#for card in simpleCards:
		#	writeCard(card, outfile)