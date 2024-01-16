import { useState } from "react";
import "./CSS/form.css";
const Form = () => {
  const [show, setShow] = useState(null);
  const [img, setImg] = useState();
  const [loading, setLoading] = useState(false);
  const [formdata, setFormdata] = useState({
    name: "",
    email: "",
    password: "",
  });
  const handleImgChange = (e) => {
    setImg(e.target.files[0]);
  };
  function handleSubmit(e, formdata) {
    setLoading(true);
    e.preventDefault();
    const ff = new FormData();
    for (const item in formdata) {
      ff.append(item, formdata[item]);
    }
    ff.append("photo", img);
    fetch(`http://localhost:5000/api/user`, {
      method: "POST",
      body: ff,
    })
      .then((res) => res.json())
      .then((res) => {
        window.alert(res.message);
        setLoading(false);
        setShow(null);
        console.log(res);
      })
      .catch((e) => {
        window.alert("error: " + e);
        setLoading(false);
      });
  }
  function mark() {
    setShow("mark");
    fetch("http://localhost:5000/api/mark-my-attendance")
      .then((res) => res.json())
      .then((res) => {
        setShow(null);
        console.log(res);
        window.alert(res.message);
      })
      .catch((e) => {
        setShow(null);
        window.alert("please try again");
      });
  }
  function handleChange(e, field) {
    //function to handle all the inputs, except image
    setFormdata({ ...formdata, [field]: e.target.value });
  }
  return (
    <div>
      {loading === true && (
        <div className="loading">loading.. please wait...</div>
      )}
      {!show && (
        <div>
          <span className="options">Choose any..</span>
          <button className="option" onClick={() => setShow("register")}>
            register
          </button>
          <button className="option" onClick={mark}>
            mark atttendance
          </button>
        </div>
      )}
      {show === "register" && (
        <div>
          <div className="form">
            <div className="subtitle">Let's create your account!</div>
            <div className="input-container ic">
              <input
                id="name"
                type="text"
                onChange={(e) => handleChange(e, "name")}
                name="name"
                className="input"
                placeholder=""
              />
              <div className="labels"></div>
              <label htmlFor="name">Name</label>
            </div>
            <div className="input-container ic">
              <input
                id="email"
                className="input"
                type="email"
                onChange={(e) => handleChange(e, "email")}
                name="email"
                placeholder=""
              />
              <div className="labels"></div>
              <label htmlFor="email">Email</label>
            </div>
            <div className="input-container ic">
              <input
                id="password"
                type="password"
                onChange={(e) => handleChange(e, "password")}
                name="password"
                className="input"
                placeholder=" "
              />
              <div className="labels"></div>
              <label htmlFor="password">password</label>
            </div>
            <div className="input-container ic">
              <input
                id="photo"
                type="file"
                name="photo"
                onChange={handleImgChange}
                className="input"
                placeholder=" "
              />
              <div className="labels"></div>
              <label htmlFor="photo">profile picture</label>
            </div>
            <br />
            <button
              onClick={(e) => handleSubmit(e, formdata)}
              className="submit"
            >
              submit
            </button>
          </div>
        </div>
      )}
      {show === "mark" && (
        <div>
          <h2>
            <b>Click</b> on the camera window press <b>Enter</b> when your name
            displays
          </h2>
          <h1>look into the camera opening in another window..</h1>
        </div>
      )}
    </div>
  );
};
export default Form;
