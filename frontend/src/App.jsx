import { Routes, Route } from "react-router-dom";
import { useState } from "react";

import Layout from "./components/Layout";

import Home from "./pages/Home";

const ROUTES = [{ path: "/", element: <Home /> }];

function App() {
  const [pagesUuidList, setPagesUuidList] = useState([]);
  console.log(2, pagesUuidList)
  const [vectorstoreUuidList, setVectorstoreUuidList] = useState([]);
  const [model, setModel] = useState("llama2");
  return (
    <div>
      <Routes>
        <Route exact path="/" element={<Layout 
                                  model={model}
                                  setModel={setModel}
                                  pagesUuidList={pagesUuidList}
                                  setPagesUuidList={setPagesUuidList}
                                  vectorstoreUuidList={vectorstoreUuidList}
                                  setVectorstoreUuidList={setVectorstoreUuidList} />}>
          <Route exact path="/" Component={(props) => <Home {...props} model={model} setModel={setModel} pagesUuidList={pagesUuidList} setPagesUuidList={setPagesUuidList} vectorstoreUuidList={vectorstoreUuidList} setVectorstoreUuidList={setVectorstoreUuidList} />} />
          {/* {ROUTES.map(({ path, element }) => (
            <Route 
            key={path}
            path={path}
            element={element}
            model={model}
            setModel={setModel}
            pagesUuidList={pagesUuidList}
            setPagesUuidList={setPagesUuidList}
            vectorstoreUuidList={vectorstoreUuidList}
            setVectorstoreUuidList={setVectorstoreUuidList} />
          ))} */}
        </Route>
      </Routes>
    </div>
  );
}

export default App;
