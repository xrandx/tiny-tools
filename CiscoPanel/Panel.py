from flask import Flask, render_template, request, jsonify, redirect, send_from_directory, session
import os
import json
from datetime import timedelta
from PanelRequest import *

app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)   
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7) 


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/validation', methods=['GET', 'POST'])
def validation():
    username, password = request.form['username'], request.form['password']
    panel_request = PanelRequest(username, password)
    if panel_request.login("https://192.168.88.10"):
        session['username'] = username
        session['password'] = password
        session['valid'] = True
        return redirect('/')
    else:
        session['valid'] = False
        return redirect('/login')


@app.route('/')
def get_panel_device(now_device=None):
    if not session.get('valid'):
        return redirect('/login')
    else:
        now_device = request.args.get('device_name')
        PanelRequest.update_hostname()
        if now_device is not None:
            session['now_device'] = now_device
        else:
            if session.get('now_device') is None:
                devices = PanelRequest.get_device_names()
                session['devices'] = devices
                session['now_device'] = devices[0]
    return render_template('panel.html')

@app.route('/panel_version', methods=['GET', 'POST'])
def panel_version():
    url = PanelRequest.get_url(session['now_device'])
    pr = PanelRequest(session['username'], session['password'])
    tmp = pr.show_version(url)
    return jsonify(tmp)


@app.route('/hostname', methods=['GET', 'POST'])
def hostname():
    url = PanelRequest.get_url(session['now_device'])
    pr = PanelRequest(session['username'], session['password'])
    hostname = request.args.get('hostname')
    pr.hostname(url, hostname)
    PanelRequest.update_hostname()
    devices = PanelRequest.get_device_names()
    session['devices'] = devices
    session['now_device'] = hostname
    return redirect('/')


@app.route('/panel_mac_address', methods=['GET', 'POST'])
def panel_mac_address():
    url = PanelRequest.get_url(session['now_device'])
    pr = PanelRequest(session['username'], session['password'])
    tmp = pr.show_mac_address_table(url)
    return jsonify(tmp)


@app.route('/panel_processes_cpu', methods=['GET', 'POST'])
def panel_processes_cpu():
    url = PanelRequest.get_url(session['now_device'])
    pr = PanelRequest(session['username'], session['password'])
    tmp = pr.show_processes_cpu(url)
    return jsonify(tmp)


@app.route('/panel_processes_memory', methods=['GET', 'POST'])
def panel_processes_memory():
    url = PanelRequest.get_url(session['now_device'])
    pr = PanelRequest(session['username'], session['password'])
    tmp = pr.show_processes_memory(url)
    return jsonify(tmp)


@app.route('/panel_interface_brief', methods=['GET', 'POST'])
def panel_interface_brief():
    url = PanelRequest.get_url(session['now_device'])
    pr = PanelRequest(session['username'], session['password'])
    tmp = pr.show_ip_interface_brief(url)
    return jsonify(tmp)


@app.route("/download_runningconfig", methods=['GET', 'POST'])
def panel_download_runningconfig():
    url = PanelRequest.get_url(session['now_device'])
    pr = PanelRequest(session['username'], session['password'])
    tmp = pr.show_running_config(url)
    dirpath = os.path.join(app.root_path, 'upload')  
    with open(dirpath + '\\runningconfig.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps(tmp))
    return send_from_directory(dirpath, "runningconfig.json", as_attachment=True)


if __name__ == '__main__':
    app.run()