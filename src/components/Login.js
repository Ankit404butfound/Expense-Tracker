import React from "react";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

const Submit = () => {
  const navigate = useNavigate("");
  const [Email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event) => {
    let Submit = true;
    if (Submit) {
      navigate("/Home");
    } else {
      alert("Invalid user ID & Password");
    }
  };
  return (
    <div className="App">
      <nav className="navbar bg-primary">
        <div className="container-fluid">
          <h1 className="navbar-brand">Room-Expense Tracker</h1>
        </div>
      </nav>

      <div className="container">
        <div className="row d-flex justify-content-center">
          <div className="col-md-4">
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <h3>Login Your Account!</h3>
                <label>Email address</label>
                <input
                  type="email"
                  className="form-control"
                  id="EmailInput"
                  name="EmailInput"
                  aria-describedby="emailHelp"
                  placeholder="Enter email"
                  onChange={(event) => Email(event.target.value)}
                />
                <small id="emailHelp" className="text-danger form-text"></small>
              </div>
              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  className="form-control"
                  id="exampleInputPassword1"
                  placeholder="Password"
                  onChange={(event) => password(event.target.value)}
                />
              </div>
              <div className="form-group form-check">
                <input
                  type="checkbox"
                  className="form-check-input"
                  id="exampleCheck1"
                />
                <label className="form-check-label">Remember Me</label>
              </div>
              <button
                type="submit"
                className="btn btn-primary"
                onSubmit={handleSubmit}
              >
                Submit
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Submit;
