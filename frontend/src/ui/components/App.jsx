// To support: theme="express" scale="medium" color="light"
// import these spectrum web components modules:
//import "@spectrum-web-components/theme/express/scale-medium.js";
//import "@spectrum-web-components/theme/express/theme-light.js";

// To learn more about using "swc-react" visit:
// https://opensource.adobe.com/spectrum-web-components/using-swc-react/
//import { Button } from "@swc-react/button";
//import { Theme } from "@swc-react/theme";

import React from "react";
import { MemoryRouter, Routes, Route } from "react-router-dom";

import Header from "./Header";
import InsertPromptPage from "./InsertPromptPage";
import IPWarning from "./BadPicture.jsx";
import GoodPicture from "./GoodPicture.jsx";
import SimilarImages from "./SimilarImages.jsx";
import Payment from "./payment";

const App = ({ sandboxProxy, addOnUISdk }) => {
  return (
    <MemoryRouter>
      <Header/>
      <Routes>
        <Route path="/" element={<InsertPromptPage sandboxProxy={sandboxProxy} />} />
        <Route path="/good-picture" element={<GoodPicture addOnUISdk={addOnUISdk} />} />
        <Route path="/bad-picture" element={<IPWarning />} />
        <Route path="/similar-Images" element={<SimilarImages />} />
        <Route path="/payment" element={<Payment />} />

      </Routes>
    </MemoryRouter>
  );
};

export default App;
