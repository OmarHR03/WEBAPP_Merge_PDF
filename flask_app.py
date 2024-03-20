from flask import Flask, render_template, request, send_file
from io import BytesIO
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfMerger
import pdfcrowd
from datetime import datetime


app = Flask(__name__, static_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def merge_pdfs():
    if request.method == 'POST':
        # Obtener los datos del formulario
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        age = request.form.get("age")
        document = request.form.get("document")
        fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        # Verificar si algún campo está vacío
        if not all([first_name, last_name, email, age, document]):
            return "Por favor complete todos los campos del formulario"


        # Generar HTML con los datos del formulario
        html_content = f"""
        <html>
    <body style="font-family: Arial, sans-serif;color: #333;font-size: 14px;line-height: 1.2;padding: 1em;">
    <div class="header space-between" style="margin-bottom: 2em;display: flex;width: 100%; justify-content: space-between;">
    <a class="logo" href="https://imgbb.com/"><img src="https://i.ibb.co/xMy0sFC/Logo-AMOM-med-1-2-1-1.jpg" alt="Logo-AMOM-med-1-2-1-1" border="0"></a>
        <div class="payee" style="text-align: left; width: 80%; ">
        <b>EMPRESA DE SERVICIOS ESPECIALIZADOS EN SALUD OCUPACIONAL (AMOM BUSINESS NETWORK)</b><br/>
                <br><strong>RNC:</strong> 1-3120107-5<br/>
                <strong>DIRECCION:</strong> CALLE A,SECTOR DON HONORIO, <br/>AV.DUARTE VIEJA<br/>
                <strong>TELEFONO:</strong> 809 - 939 - 2159<br/>
                <strong>EMAIL:</strong>amombusinessnetwork@gmail.com<br/>
        </div>
    </div>
    <hr style="margin: 20px 0;border: 0;border-bottom: 1px solid #e3e3e3;"/>
    <div class="billing-details space-between" style="margin: 2em 0;">
        <div class="payor" style="text-align: left;">
        Cobrar a :<br/>
        <b>AMOM BUSINESS NTEWORK</b><br/>
                c/o Person Name<br/>
                Santo Domingo, Distrito Nacional<br/>
                Republica Dominicana<br/>
        </div>
        
    </body>
    <hr style="margin: 20px 0;border: 0; border-bottom: 1px solid #e3e3e3;"/>

    <div class="info" style="text-align: center; padding:30px; font-size:15px;">
        <strong> INFORMACIONES GENERALES
    </div>

    <div class="container" style="display: flex; justify-content: space-between;">
        <table class="info-table1" style="flex: 1; border-collapse: collapse; margin-right: 20px ;">
        <tbody>
            <tr style="padding: 10px; border: 1px solid #e3e3e3">
            <td style="font-size:12px;padding: 10px; border: 1px solid #e3e3e3">
                <strong>NOMBRES <br>DEL PACIENTE:</br></strong>
            </td>
            <td style="padding: 10px;font-size:13px;">{first_name}</td>
            </tr>
            <tr style=" padding:10px; border: 1px solid #e3e3e3">
            <td style="font-size:12px;padding: 10px; border: 1px solid #e3e3e3">
                <strong>APELLIDO <br>DEL PACIENTE</br></strong>
            </td>
            <td style="padding: 10px; font-size:13px;">{last_name}</td>
            <tr>
            <tr style="padding: 10px; border: 1px solid #e3e3e3">
            <td style="font-size:12px; padding: 10px; border: 1px solid #e3e3e3">
                <strong>EMAIL:</strong>
            </td>
            <td style="padding: 10px;font-size:13px;">{email}</td>
            </tr>

            <tr style="padding: 10px; border: 1px solid #e3e3e3">
            <td style="font-size:12px;padding: 10px; border: 1px solid #e3e3e3">
                <strong>EDAD:</strong>
            </td>
            <td style="padding: 10px;font-size:13px;">{age} años</td>
            <tr>
        </tbody>
        </table>

        <table class="info-table2" style=" width: 50%; padding: 10px; border: 1px solid #e3e3e3; flex: 1; border-collapse: collapse; margin-right: 20px ;">
        <tbody>
            <tr style="padding: 10px; border: 1px solid #e3e3e3">
            <td style="font-size:12px;padding: 10px; border: 1px solid #e3e3e3">
                <strong>DOCUMENTO DE IDENTIDAD:</strong>
            </td>
            <td style="padding: 10px;font-size:13px;">{document}</td>
            </tr>
            <tr style="padding: 10px; border: 1px solid #e3e3e3">
            <td style="font-size:12px;padding: 10px; border: 1px solid #e3e3e3">
                <strong>FECHA ACTUAL</strong>
            </td>
            <td style="padding: 10px;font-size:13px;">{fecha_actual}</td>
            </tr>
            <tr style="padding: 10px; border: 1px solid #e3e3e3">
            <td style="font-size:12px;padding: 10px; border: 1px solid #e3e3e3">
                <strong>CARGO:</strong>
            </td>
            <td style="padding: 10px;font-size:13px;">AREA LEGAL</td>
            </tr>

            <tr style="padding: 10px; border: 1px solid #e3e3e3">
            <td style="font-size:12px;padding: 10px; border: 1px solid #e3e3e3">
                <strong>CONTRATO No 462:</strong>
            </td>
            <td style="padding: 10px;font-size:13px;">AMOM BUSINESS NETWORK EIRL: CONSOLIDADO</td>
            </tr>
        </tbody>
        </table>
    </div>

    </html>

        """

        
        # Convertir el HTML a PDF utilizando pdfcrowd
        pdf_buffer = BytesIO()
        client = pdfcrowd.HtmlToPdfClient("omarhr03", "e38cb86702620abc33c643a85f80a1aa")
        client.setPageWidth("210mm")
        client.setPageHeight("297mm")
        pdf_buffer.write(client.convertString(html_content))

        # Crear un buffer para escribir el PDF final
        buffer = BytesIO()

        # Fusionar el PDF local con el HTML en un solo PDF
        merger = PdfMerger()
        merger.append(fileobj=pdf_buffer)

        # Obtener los archivos PDF seleccionados
        pdf_files = request.files.getlist("pdf_files")

        # Agregar los archivos PDF seleccionados al PDF final
        for pdf_file in pdf_files:
            merger.append(pdf_file)

        # Escribir el PDF final en el buffer
        merger.write(buffer)
        buffer.seek(0)

        # Permitir que el archivo se descargue
        return send_file(buffer, as_attachment=True, download_name="merged.pdf")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
