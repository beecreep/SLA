from flask import render_template, Blueprint, send_from_directory

materias_bp = Blueprint('materias', __name__)

@materias_bp.route('/historia')
def historia():
    return render_template('materias.html/historia.html')

@materias_bp.route('/portugues')
def portugues():
    return render_template('materias.html/portugues.html')

@materias_bp.route('/geografia')
def geografia():
    return render_template('materias.html/geografia.html')

@materias_bp.route('/matematica')
def matematica():
    return render_template('materias.html/matematica.html')

@materias_bp.route('/fisica')
def fisica():
    return render_template('materias.html/fisica.html')

@materias_bp.route('/quimica')
def quimica():
    return render_template('materias.html/quimica.html')

@materias_bp.route('/biologia')
def biologia():
    return render_template('materias.html/biologia.html')

@materias_bp.route('/ingles')
def ingles():
    return render_template('materias.html/ingles.html')

@materias_bp.route('/st')
def st():
    return render_template('materias.html/curso-sites/st.html')

@materias_bp.route('/adm')
def adm():
    return render_template('materias.html/curso-sites/adm.html')

@materias_bp.route('/eventos')
def eventos():
    return render_template('materias.html/curso-sites/eventos.html')

@materias_bp.route('/eletronica')
def eletronica():
    return render_template('materias.html/curso-sites/eletronica.html')

@materias_bp.route('/pdf/view/<path:subpath>/<filename>')
def view_pdf(subpath, filename):
    # 'subpath' permite acessar subpastas
    return send_from_directory(f'pdfs/{subpath}', filename)

@materias_bp.route('/pdf/download/<path:subpath>/<filename>')
def download_pdf(subpath, filename):
    # 'subpath' permite acessar subpastas
    return send_from_directory(f'pdfs/{subpath}', filename, as_attachment=True)
    
