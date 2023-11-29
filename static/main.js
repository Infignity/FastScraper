// my javascript functions
(function() {
    console.log('checker setup');
})();
  
document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById("myForm").addEventListener("submit", function (e) {
        e.preventDefault();
        const fileInput = document.getElementById('file');
        const selectedFile = fileInput.files[0];
        const formData = new FormData();

        formData.append('file', selectedFile);

        fetch('/scrape', {
            method: 'POST',
            body: formData
        })
            .then(resp => resp.text())
            .then(data => {
                getStatusTask(data.task_id)

            })
            .catch(error => {
                console.error(error);
            });

    });

});

const getStatusTask = (taskID) => {
    fetch(`/tasks/${taskID}`, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(res => {
        console.log(res)
        const html = `
            <div class="card m-3" style="width: 18rem;">
                <div class="card-body">
                <h5 class="card-title">Task-Id ${taskID}</h5>
                <p class="card-text">status: ${res.state} </p>
                <a href="/specific-task/${taskStatus }" class="btn btn-outline-success">view</a>
                </div>
            </div>
        `;
        const tasksDiv = document.getElementById('tasks');
        tasksDiv.innerHTML = html;

        const taskStatus = res.task_status;
        if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
        setTimeout(function() {
        getStatus(res.task_id);
        }, 2000);
    })
    .catch(err => console.log(err));
} 

// Function to generate a random UUID
const generateUUID = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = (Math.random() * 16) | 0;
        const v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}

async function handleDownload() {
        try {
            // Fetch the task_id from the template
            const task_id = "{{ task_id }}";

            // Fetch the CSV file using FastAPI endpoint with task_id
            const response = await fetch(`/download-csv/${task_id}`);

            // Check if the response is successful
            if (response.ok) {
                // Convert the response to a Blob
                const blob = await response.blob();

                // Generate a random UUID for the CSV file
                const uuid = generateUUID();

                // Create a temporary link to trigger the download
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = `tasks_${task_id}_${uuid}.csv`;

                // Trigger a click on the link to initiate the download
                link.click();
            } else {
                console.error('Failed to fetch CSV file:', response.statusText);
            }
        } catch (error) {
            console.error('Error during CSV download:', error);
        }
    }

// Attach the handleDownload function to the button click event
document.getElementById('downloadBtn').addEventListener('click', handleDownload);
