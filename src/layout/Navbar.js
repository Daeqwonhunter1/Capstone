import React, { useEffect, useState } from "react";

export default function Navbar() {

    const [state, setState] = useState({
        val:''
    })

    const handleChange = (e) => {
        console.log(e.target.value)
        setState({value: e.target.value})
    }


  return (
    <div id="container">
      {/* If signed in show navbar */}
      <div className="d-xl-inline-flex">
        <span className="input-group-text" id="addon-wrapping">
          @
        </span>
        <input
          type="text"
          className="form-control"
          placeholder="Movie"
          aria-label="Movie"
          aria-describedby="addon-wrapping"
          value ={state.val}
          onChange={(e) => handleChange(e)}
        />
        <input type="submit" />
      </div>
    </div>
  );
}
