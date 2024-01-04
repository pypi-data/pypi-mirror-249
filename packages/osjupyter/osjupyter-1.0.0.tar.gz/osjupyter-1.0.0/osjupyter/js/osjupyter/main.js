define([
  "base/js/namespace",
  "base/js/events",
  "https://cdn.socket.io/4.7.2/socket.io.min.js",
], (Jupyter, events, io) => {
  const load_ipython_extension = () => {
    let socket;
    let userClientId;
    let notebookClientId;
    const chromeExtID = "oapkeobjlhimhjkfmhnceapdflfnnpjl";

    /*

    Chrome Bridge

    */

    // This code should be part of your Jupyter Notebook extension
    const getSessionId = () => {
      // Sending a message to the content script
      chrome.runtime.sendMessage(
        chromeExtID,
        { message: "getSessionId" },
        (response) => {
          // Store User Client ID
          userClientId = `${response.sessionId}+user`;
          // Store Notebook Client ID
          notebookClientId = `${response.sessionId}+notebook`;
          // Initialize web socket
          socketInit();
        }
      );
    };

    /* 

    Jupyter Notebook management

    */

    const insertCodeCell = (code, index) => {
      // Access the Jupyter notebook
      const notebook = Jupyter.notebook;

      // Determine the position where the cell will be added
      const cellIndex = index !== undefined ? index : notebook.ncells();

      // Insert a code cell at the specified index
      notebook.insert_cell_at_index("code", cellIndex);

      // Set the cell's code
      const cell = notebook.get_cell(cellIndex);
      cell.set_text(code);

      // Optionally, you might want to render the cell
      cell.execute();
    };

    // Function to load a CSS file
    const loadCSS = (filename) => {
      var fullPath = require.toUrl("./" + filename);
      var link = document.createElement("link");
      link.href = require.toUrl("../nbextensions/osjupyter/" + filename);
      link.type = "text/css";
      link.rel = "stylesheet";
      document.getElementsByTagName("head")[0].appendChild(link);
    };

    // Function to handle notebook change events
    const onNotebookChanged = (event, data) => {
      // console.log('Notebook changed:', event, data);
      if (event.type === "create") {
        // console.log("New cell created", event);
        const content = getNotebookContent();
      }

      if (event.type === "delete") {
        // console.log("Cell deleted", event);
        const content = getNotebookContent();
      }
      // You can add your custom logic here to handle the change
    };

    const initNotebookEvent = () => {
      // Listen for events related to notebook changes
      // events.on('notebook_saved.Notebook', onNotebookChanged);
      // events.on('notebook_renamed.Notebook', onNotebookChanged);
      events.on("create.Cell", onNotebookChanged);
      events.on("delete.Cell", onNotebookChanged);
      // events.on('execute.CodeCell', onNotebookChanged);
      // events.on('select.Cell', onNotebookChanged);
      // events.on('edit_mode.Cell', onNotebookChanged);
      // events.on('command_mode.Cell', onNotebookChanged);
    };

    const getNotebookContent = () => {
      // Access the current notebook
      const notebook = Jupyter.notebook;

      // Get the entire notebook's JSON data
      const notebookContent = notebook.toJSON();

      // This JSON object can be converted to a string if needed
      // const notebookContentStr = JSON.stringify(notebookContent, null, 2);

      // Log the content to console or use it as needed
      // console.log(notebookContentStr);

      // If you need to return this data from the function
      return notebookContent;
    };

    // Function to update the icon class
    const updateIconClass = (connected) => {
      var iconElement = $(".os-icon");
      if (connected) {
        iconElement.removeClass("icon-disconnected").addClass("icon-connected");
      } else {
        iconElement.removeClass("icon-connected").addClass("icon-disconnected");
      }
    };

    const socketInit = function () {
      // Initialize WebSocket connection
      socket = io("https://os-sockets-dot-osyris-1a1e5.uc.r.appspot.com", {
        query: { clientId: notebookClientId },
      });

      socket.on("connect", function () {
        console.log("Web socket connected!");
        // Toggle Icon
        updateIconClass(true);

        // Add cell event
        socket.on("add_cell", async (data) => {
          try {
            insertCodeCell(data.code);
          } catch (error) {
            console.error("Error parsing JSON:", error);
          }
        });

        // Event when the socket disconnects
        socket.on("disconnect", function () {
          console.log("Disconnected from the WebSocket server");
          updateIconClass(false);
        });
      });

      // Additional socket.io logic here
    };

    const action = {
      icon: "fa os-icon icon-disconnected",
      id: "osyris-icon",
      help: "Connect to Osyris",
      help_index: "zz",
      handler: getSessionId,
    };
    const prefix = "osyris";
    const action_name = "show-alert";

    const full_action_name = Jupyter.actions.register(
      action,
      action_name,
      prefix
    );
    Jupyter.toolbar.add_buttons_group([full_action_name]);
    initNotebookEvent();
    // Load CSS file
    loadCSS("style.css");
  };

  return {
    load_ipython_extension: load_ipython_extension,
  };
});
