from flet import *
from firebase_admin import credentials, initialize_app, storage
import os

# THIS GET FROM SRVICE_ACCOUNT.JSON FROM FIREBASE ADMIN
mycred = credentials.Certificate("service_account.json")

# ADD URL STORAGE FROM FIREBASE ADMIN DASHOBORD

# YOU MUST REMOVE gs:// FROM URL gs://testdoang-e8396.appspot.com

initialize_app(mycred, {'storageBucket':'flet-firebase-ced4d.appspot.com'})

def main(page: Page):

	def upload_now(e:FilePickerResultEvent):
		for x in e.files:
			try:
				fileName = x.path
				bucket = storage.bucket()
				blob = bucket.blob(os.path.basename(fileName))
				blob.upload_from_filename(fileName)

				# AND THIS OPTIONAL IF YOU WANT CREATE IMAGE URL
				# IS PUBLIC OR NOT
				blob.make_public()

				# AND IF SUCCESS UPLOAD TO storage THEN SHOW SNACKBAR
				page.snack_bar = SnackBar(
					Text("Success uploading !!!!!"),
					bgcolor="green"

					)
				page.snack_bar.open = True
				page.update()
				print("YOU SUCECSS UPLOADING!!!!")
				print("YOu image FIle url IS  = ", blob.public_url)
			except Exception as e:
				print(e)
				print("YOU FAILEDDD UPLOAD !!!!")

	file_picker = FilePicker(
		on_result=upload_now
	)

	page.overlay.append(file_picker)
	page.add(
	Column([
			Text("Upload file to firebase", size=30),
			ElevatedButton(
				"upload file now",
				bgcolor="blue",
				color="white",
				on_click=lambda e:file_picker.pick_files()
			)
		])
	)

flet.app(target=main)