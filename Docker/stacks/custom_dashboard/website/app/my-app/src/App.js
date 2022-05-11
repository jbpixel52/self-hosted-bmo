import "./App.css";
import { greeting, date } from "./dynamics.js";
import { box } from "./boxapp.js";


function App() {
  return (
    <div className="App" id="root">
      <div class="header">
        {greeting()}
        {date()}
      </div>

      <div class="boxes" id="boxes">
        {box("Dashboard", "https://dashboard.jbpixel.xyz", "LOREM IPSUM")}
        {box("Sonarr", "https://sonarr.jbpixel.xyz", "LOREM IPSUM")}
      </div>
    </div>
  );
}

export default App;
