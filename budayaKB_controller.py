"""
TEMPLATE TP4 DDP1 Semester Gasal 2019/2020

Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@cs.ui.ac.id)

Last update: 23 November 2019

"""
from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template, redirect, flash

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()


#merender tampilan default(index.html)
@app.route('/')
def index():
	return render_template("index.html")

# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 	
@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
	if request.method == "GET":
		return render_template("imporBudaya.html")

	elif request.method == "POST":
		try:
			f = request.files['file']
			databasefilename=f.filename
			result_impor=budayaData.importFromCSV(f.filename)
			budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
			return render_template("imporBudaya.html", result=result_impor, fname=f.filename)
		except:
			text_impor = "Sepertinya terjadi Error, entah itu file bukan csv, atau GUI local tidak mengenali file"
			return render_template("imporBudaya.html", text = text_impor)

# Bagian ini nyari nama di file
@app.route('/cariBudaya', methods=['GET', 'POST'])
def cariBudaya():
	if request.method == "GET":
		return render_template("cariBudaya.html")
	elif request.method == "POST":
		budayaTipe = request.form["budaya"]
		namaBudaya = request.form["userType"]
		# masuk kedalah program
		if budayaTipe == "nama":
			nama = budayaData.cariByNama(namaBudaya)
			list_nama = []
			if len(nama) > 0:
				for item in nama:
					list_nama.append(str(item).split(','))
					text_result = "Ditemukan {} Budaya dalam dataBudaya".format(len(list_nama))
				return render_template("cariBudaya.html", result = list_nama, text = text_result)
			else:	
				text_result = "sepertinya yang anda cari tidak ada."		
				return render_template("cariBudaya.html", text=text_result)
		elif budayaTipe == "tipe":
			tipe = budayaData.cariByTipe(namaBudaya)
			if len(tipe) > 0:
				list_tipe = []
				for item in tipe:
					list_tipe.append(str(item).split(','))
				text_result = "ditemukan {} budaya di dalam data base kami.".format(len(list_tipe))
				return render_template("cariBudaya.html", result = list_tipe, text=text_result)
			else:
				text_result = "sepertinya yang anda cari tidak ada"
				return render_template("cariBudaya.html", text=text_result)
		elif budayaTipe == "prov":
			prov = budayaData.cariByProv(namaBudaya)
			if len(prov) > 0:
				list_prov = []
				for item in prov:
					list_prov.append(str(item).split(','))
				text_result = "ditemukan {} budaya dari provinsi {}".format(len(list_prov), namaBudaya)
				return render_template("cariBudaya.html", result = list_prov, text=text_result)
			else:
				text_result = "sepertinya yang anda cari tidak ada di dataBase kami"
				return render_template("cariBudaya.html", text=text_result)

# Bagian ini tambahBudaya ke file
@app.route('/tambahBudaya', methods=['GET', 'POST'])
def tambahBudaya():
	if request.method == "GET":
		return render_template("tambahBudaya.html")

	elif request.method == "POST":
		nama = request.form['nama']
		tipe = request.form['tipe']
		prov = request.form['prov']
		url = request.form['url']
		result = budayaData.tambah(nama, tipe, prov, url)
		if result == 1:
			text_result = "sukses menambahkan data '{}'".format(nama)
		else:
			text_result = "sepertinya data anda sudah ada di dalam sistem"
		return render_template("tambahBudaya.html", text=text_result)

# Bagian ini ubahBudaya yang ada di file
@app.route('/ubahBudaya', methods=['GET', 'POST'])
def ubahBudaya():
	if request.method == 'GET':
		return render_template('ubahBudaya.html')
	elif request.method == 'POST':
		nama = request.form['nama']
		tipe = request.form['tipe']
		prov = request.form['prov']
		url = request.form['url']
		result = budayaData.ubah(nama, tipe, prov, url)
		if result == 1:
			text_result = "Sukses mengubah data '{}'".format(nama)
		else:
			text_result = "data dengan nama '{}' tersebut tidak ada dalam sistem".format(nama)
		return render_template('ubahBudaya.html', text=text_result)

# Bagian ini hapusBudaya yang ada di file
@app.route('/hapusBudaya', methods=['GET', 'POST'])
def hapusBudaya():
	if request.method == 'GET':
		return render_template('hapusBudaya.html')
	elif request.method == 'POST':
		nama = request.form['nama']
		result = budayaData.hapus(nama)
		if result == 1:
			text_result = "Sukses menghapus data '{}'".format(nama)
		else:
			text_result = "Data dengan nama '{}' tersebut tidak ada".format(nama)
		return render_template('hapusBudaya.html', text=text_result)

# Bagian ini stat menampilkan statistik dari data
@app.route('/statsBudaya', methods=['GET', 'POST'])
def statsBudaya():
	if request.method == 'GET':
		return render_template('statsBudaya.html')
	elif request.method == 'POST':
		userCommend = request.form['stat']
		if userCommend == 'all':
			result_impor = budayaData.stat()
		elif userCommend == 'Tipe':
			result_impor = budayaData.statByTipe()
		elif userCommend == 'Provinsi':
			result_impor = budayaData.statByProv()
		return render_template('statsBudaya.html', result= result_impor, user= userCommend)

# selsai
# run main app
if __name__ == "__main__":
	app.run(debug=True)



