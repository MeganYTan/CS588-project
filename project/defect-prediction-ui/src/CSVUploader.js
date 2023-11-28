import React, { useState } from 'react';
import Papa from 'papaparse';

function CSVUploader() {
    const [total, setTotal] = useState([1]);
    const [openAIResponse, setopenAIResponse] = useState("");
    const [data, setData] = useState({});

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('file', file);

        fetch('http://localhost:5000/upload-csv', {
            method: 'POST',
            body: formData,
        })
            .then(response => {
                console.log(response);
                if (response.ok) {
                    return response.json();
                } else {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Server error');
                    });
                }
            })
            .then(data => {
                setTotal(data.total_defects);
                setopenAIResponse(data.open_AI_response);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };
    const get = (event) => {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('file', file);

        fetch('http://localhost:5000', {
            method: 'GET',
            // body: formData,
        })
            .then(response => {
                console.log(response);
                if (response.ok) {
                    return response.json();
                } else {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Server error');
                    });
                }
            })
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };


    const getCSVData = (file) => {
        Papa.parse(file, {
            complete: (result) => {
                console.log(result);
                setData(result.data);
            },
            header: true
        });
    };

    return (
        <>
            <input type="file" accept=".csv" onChange={handleFileChange} />
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: "25vh", width: "60vw", marginLeft: "20vw" }}>
                <div>
                    <h2>Random Forest Regression</h2>
                    <div>Total:{total}</div>

                </div>
                <div>
                    <h2>OpenAI API Prediction</h2>
                    <span>{openAIResponse}</span>
                </div>
            </div>
        </>
    );
}

export default CSVUploader;
