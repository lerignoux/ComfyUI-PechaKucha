import { app } from "../../../scripts/app.js";

app.registerExtension({
  name: "pecha_kucha.DownloadPechaKucha",
  nodeCreated(node) {
    if (node.comfyClass !== "DownloadPechaKucha") return;
    console.log("Creating DownloadPechaKucha node.");

    const onExecuted = node.onExecuted;

    node.onExecuted = function (message) {
      onExecuted?.apply(this, arguments);

      let filePath = message.text[0];
      console.log(`Powerpoint path received : ${filePath}`);

      if (!filePath) {
        const msg = "Unable to get presentation File path.";
        console.error(msg);
        useToastStore().addAlert(msg);
      }

      const modelWidget = node.widgets?.find(
        (w) => w.name === "Open Presentation",
      );

      if (modelWidget) {
        modelWidget.value = filePath.replaceAll("\\", "/");
        modelWidget.disabled = false;
      }
    };

    const download = () => {
      let filePath = "";

      const fileNameWidget = node.widgets?.find(
        (w) => w.name === "Open Presentation",
      );
      if (!fileNameWidget) {
        console.error("Could not find Open presentation widget.");
      }
      filePath = fileNameWidget.value;
      if (!filePath) {
        console.error(`Could not find presentation file: ${filePath}`);
      }

      console.log("Downloading presentation:", filePath);

      // Remove any leading ./output/ prefix if present
      const cleanFilePath = filePath.replace(/^\.\/output\//, "");
      const folderName = cleanFilePath.replace(/[^\\/]+$/, "");
      const fileNameMatch = cleanFilePath.match(/[^\\/]+$/);
      const fileName = fileNameMatch ? fileNameMatch[0] : "";
      const viewUrl = `api/view?subfolder=${encodeURIComponent(folderName)}&filename=${encodeURIComponent(fileName)}&type=output`;

      // Open the presentation in a new tab
      window.open(viewUrl, "_blank");
    };

    // Create the button widget (initially disabled until we get the presentation file available)
    const downloadButton = node.addWidget(
      "button",
      "Open Presentation",
      "",
      download,
    );
    downloadButton.disabled = true;
    node.downloadButton = downloadButton;
  },
});
