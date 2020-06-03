import json

from flask import Flask
from tika import parser

from typing import Dict, List


AUTO_REFRACTION_RESULTS = slice(1,4)
KERATOMETRY_RESULTS = slice(5,11)
PATIENT_DATA = slice(11,14)

def extract_results() -> Dict[str, Dict[str, str]]:
    raw: Dict[str, str] = parser.from_file("vv.pdf")
    visuref: List[str] = [line for line in raw['content'].strip().splitlines() if line]
    auto_refraction: List[str] = [tuple(result.split()) for result in visuref[AUTO_REFRACTION_RESULTS]]
    keratometry: List[str] = [tuple(result.split()) for result in visuref[KERATOMETRY_RESULTS]]
    final: Dict[str, Dict[str, str]] = {}

    for index in range(len(auto_refraction)):
        description: str = auto_refraction[index][1]
        od_result: str = auto_refraction[index][0]
        oe_result: str = auto_refraction[index][2]
        final.update({
            description: {
                'OD': od_result,
                'OE': oe_result
            }
        })

    for index in range(len(keratometry)):
        description: str = " ".join(keratometry[index][1:4])
        od_result: str = keratometry[index][0]
        oe_result: str = keratometry[index][4]
        final.update({
            description: {
                'OD': od_result,
                'OE': oe_result
            }
        })

    result_dumped: str = json.dumps(final, indent=2)
    return json.loads(result_dumped)

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

@app.route("/")
def index() -> Dict[str, Dict[str, str]]:
    return extract_results()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)

