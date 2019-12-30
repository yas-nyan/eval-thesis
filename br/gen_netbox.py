
text = "address,tenant,status,description\n"


for i in range(1,4):
	#addr = f"202.0.73.{50+i}/25"
	addr = f"2001:200:0:8831:feee:caca:{i}/64"
	hostname = f"rr{str(i).zfill(2)}.sfc.wide.ad.jp"
	text += f"{addr},yas-nyan,Reserved,{hostname}\n"

print(text)
