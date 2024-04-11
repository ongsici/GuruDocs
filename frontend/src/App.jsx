import { Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";

import Home from "./pages/Home";

const ROUTES = [{ path: "/", element: <Home /> }];

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Layout />}>
          {ROUTES.map(({ path, element }) => (
            <Route key={path} path={path} element={element} />
          ))}
        </Route>
      </Routes>
    </div>
  );
}

export default App;
