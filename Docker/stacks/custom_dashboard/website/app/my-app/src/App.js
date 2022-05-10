import './App.css';
import { greeting, getTime } from "./dynamics.js";
import {box} from './boxapp.js'
function App() {
  return (
    <div className="App">
    
    <div class='header'>{greeting()}{getTime()}</div>

    {box('Dashboard','https://dashboard.jbpixel.xyz','LOREM IPSUM')}
    <div></div>







    </div>);
}

export default App;
