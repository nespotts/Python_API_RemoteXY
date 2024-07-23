import requests
from bs4 import BeautifulSoup
from datastream_html import rv_battery_html, rv_brain_html


	# response = requests.get("https://blynk.cloud/dashboard/52834/templates/edit/288956/datastreams")
class createBlynkDatastreams:
	datastreams = {}
	txt_file_name = ''
	
	def __init__(self) -> None:
		pass

	def process_html(self, selector):
		if selector == 1:
			html = rv_brain_html
			txt_file_name = "rv_brain_html.txt"
		elif selector == 2:
			html = rv_battery_html
			txt_file_name = "rv_battery_html.txt"

	 
		soup = BeautifulSoup(html, features="html.parser")
		rows = soup.select("#datastreams-table > div > div.ant-table-body > table > tbody > tr.ant-table-row")

		datastreams = {}
		# print(rows)
		for row in rows:
			name = row.select_one("td.ant-table-cell.table-cell-name.ant-table-cell-fix-left.ant-table-cell-fix-left-last.ant-table-cell-ellipsis > span > span")
			pin = row.select_one("td:nth-child(5)")
			# datastreams.append(name.text)


			# form: datastream_value=0
			# self.rv_battery_datastreams.append(f"{name.text}=0")
	 			# datastreams[pin.text] = {
			# 	"name": name.text,
			# 	"pin": pin.text
			# }
   
			key = name.text.replace(" ", "_")
			key = key.lower()

			self.datastreams[key] = 0 

		# write lines to text file
		with open("variables.txt", "a") as f:
			for key, value in self.datastreams.items():
				f.write(f"{key}={value}\n")
			
		print(self.datastreams)

		 

# print(response.text)

if __name__ == "__main__":
	d = createBlynkDatastreams()
	d.process_html(1)
	d.process_html(2)