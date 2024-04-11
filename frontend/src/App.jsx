import { Routes, Route } from "react-router-dom";
import { useState } from "react";

import Layout from "./components/Layout";

import Home from "./pages/Home";

const ROUTES = [{ path: "/", element: <Home /> }];

function App() {
  const [pagesUuidList, setPagesUuidList] = useState([]);
  const [vectorstoreUuidList, setVectorstoreUuidList] = useState([]);
  const [fileName, setFileName] = useState(null);
  const [model, setModel] = useState("llama2");
  console.log(2, "pages", pagesUuidList)
  console.log(2, "vector", vectorstoreUuidList)
  return (
    <div>
      <Routes>
        <Route exact path="/" element={<Layout 
                                  model={model}
                                  setModel={setModel}
                                  pagesUuidList={pagesUuidList}
                                  setPagesUuidList={setPagesUuidList}
                                  vectorstoreUuidList={vectorstoreUuidList}
                                  setVectorstoreUuidList={setVectorstoreUuidList}
                                  fileName = {fileName}
                                  setFileName={setFileName} />}>
          <Route exact path="/" Component={(props) => <Home {...props} 
                                                      model={model} 
                                                      setModel={setModel} 
                                                      pagesUuidList={pagesUuidList} 
                                                      setPagesUuidList={setPagesUuidList} 
                                                      vectorstoreUuidList={vectorstoreUuidList} 
                                                      setVectorstoreUuidList={setVectorstoreUuidList}
                                                      fileName = {fileName}
                                                      setFileName={setFileName} />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
