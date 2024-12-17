function loadSection(section) {
  const mainContent = document.getElementById('main-content');

  switch (section) {
    case 'ticketGW':
      mainContent.innerHTML = `
        <h2>Ticket GW</h2>
        <div class="mb-3">
          <label for="ticketId" class="form-label">Enter Ticket ID</label>
          <input type="text" class="form-control" id="ticketId" placeholder="Ticket ID">
        </div>
        <button class="btn btn-primary" onclick="alert('Ticket submitted')">Submit</button>
      `;
      break;

    case 'systemRefresh':
      mainContent.innerHTML = `
        <h2>System Refresh</h2>
        <div class="mb-3">
          <label for="taskType" class="form-label">Select Task</label>
          <select class="form-select" id="taskType">
            <option value="refresh">Refresh</option>
            <option value="complete">Complete</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="additionalInput" class="form-label">Enter Additional Input</label>
          <input type="text" class="form-control" id="additionalInput" placeholder="e.g., IP Address or Task Name">
        </div>
        <button class="btn btn-success" onclick="handleSystemTask()">Execute</button>
      `;
      break;

    case 'deleteBundles':
      mainContent.innerHTML = `
        <h2>Delete Bundles</h2>
        <div class="mb-3">
          <label for="location" class="form-label">Select Location</label>
          <select class="form-select" id="location">
            <option value="local">Local</option>
            <option value="enterprise">Enterprise</option>
          </select>
        </div>
        <button class="btn btn-danger" onclick="alert('Bundle deleted')">Delete</button>
      `;
      break;

    default:
      mainContent.innerHTML = `<p>Select a valid task from the sidebar.</p>`;
      break;
  }
}

function handleSystemTask() {
  const taskType = document.getElementById('taskType').value;
  const additionalInput = document.getElementById('additionalInput').value;

  if (!additionalInput) {
    alert("Please provide the required additional input!");
    return;
  }

  alert(`Task "${taskType}" executed with input: ${additionalInput}`);
}
