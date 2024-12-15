// JavaScript to dynamically load sections
function loadSection(section) {
  const mainContent = document.getElementById('main-content');

  switch (section) {
    case 'ticketGW':
      mainContent.innerHTML = `
        <h2>Ticket GW</h2>
        <label for="ticketId">Enter Ticket ID:</label>
        <input type="text" id="ticketId" placeholder="Ticket ID">
        <button onclick="handleTicket()">Submit</button>
      `;
      break;

    case 'systemRefresh':
      mainContent.innerHTML = `
        <h2>System Refresh/Complete Task</h2>
        <label for="taskType">Select Task:</label>
        <select id="taskType">
          <option value="refresh">Refresh</option>
          <option value="complete">Complete</option>
        </select>
        <button onclick="handleSystemTask()">Execute</button>
      `;
      break;

    case 'deleteBundles':
      mainContent.innerHTML = `
        <h2>Delete Bundles</h2>
        <label for="location">Select Location:</label>
        <select id="location">
          <option value="local">Local</option>
          <option value="enterprise">Enterprise</option>
        </select>
        <button onclick="handleDelete()">Delete</button>
      `;
      break;

    case 'billingActivation':
      mainContent.innerHTML = `
        <h2>Billing Activation</h2>
        <label for="billingToggle">Activate Billing:</label>
        <select id="billingToggle">
          <option value="local">Local</option>
          <option value="remote">Remote</option>
        </select>
        <button onclick="handleBilling()">Activate</button>
      `;
      break;

    case 'taskCompletion':
      mainContent.innerHTML = `
        <h2>Task Completion</h2>
        <label for="taskId">Enter Task ID:</label>
        <input type="text" id="taskId" placeholder="Task ID">
        <button onclick="handleCompletion()">Complete</button>
      `;
      break;

    case 'errorTracking':
      mainContent.innerHTML = `
        <h2>Error Tracking</h2>
        <label for="errorSearch">Search Logs:</label>
        <input type="text" id="errorSearch" placeholder="Keyword or Timestamp">
        <button onclick="handleErrorSearch()">Search</button>
      `;
      break;

    case 'specUpdate':
      mainContent.innerHTML = `
        <h2>Spec Update</h2>
        <textarea id="specDetails" placeholder="Enter spec details..."></textarea>
        <button onclick="handleSpecUpdate()">Update</button>
      `;
      break;

    case 'statusQuery':
      mainContent.innerHTML = `
        <h2>Status/Errors Query</h2>
        <label for="queryType">Select Query Type:</label>
        <select id="queryType">
          <option value="status">Status</option>
          <option value="error">Error</option>
        </select>
        <button onclick="handleQuery()">Run Query</button>
      `;
      break;

    case 'infoSelect':
      mainContent.innerHTML = `
        <h2>Info/Select</h2>
        <label for="infoSearch">Search Information:</label>
        <input type="text" id="infoSearch" placeholder="Search...">
        <button onclick="handleInfo()">Search</button>
      `;
      break;

    default:
      mainContent.innerHTML = `<p>Select a valid task from the sidebar.</p>`;
      break;
  }
}
