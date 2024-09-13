from flask import Blueprint, request, jsonify
import json

from services.BackendData import getBackendData, listData, LineData

BackendData = Blueprint('BackendData', __name__)


@BackendData.route('/getData', methods=['POST'])
def getData():
    return getBackendData()


@BackendData.route('/Bie', methods=['POST'])
def getListData():
    return listData()


@BackendData.route('/Line', methods=['POST'])
def getLineData():
    return LineData()
