import React,{useState} from 'react';
import PasswordStrengthMeter from './PasswordStrengthMeter';

const App = () => {
  const [userInfo, setuserInfo] = useState({
    password: '',
  });

  const [password, setPassword] = useState("");
  const [confirmedPassword, setConfirmedPassword] = useState("");
  const [Error, setError] = useState(null);
  const [email, setEmail] = useState("");
  const [errorMsg, setErrorMsg] = useState(null);
  const [isError, setIsError] = useState(null);

  function handleChange(event) {
    setEmail(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (regex.test(email)) {
      alert("Email is valid");
    } else {
      setErrorMsg("Please enter a valid email address");
    }
  }


  const handleEmailAddress = (e) =>{
    e.preventDefault()
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (regex.test(email)) {
      alert("Email is valid");
      setEmail(e.target.value);
    } else {
      setErrorMsg("Please enter a valid email address");
    }

  }
  const handleName = (e) => {

  }

  function confirmPassword(e) {
    setConfirmedPassword(e.target.value);
    if (e.target.value !== password) {
      setError("Passwords do not match")
    } else {
      setError("Passwords do match")
    }
  }

  const handleChangePassword = (e) => {
    let password  = e.target.value;
    setuserInfo({
      ...userInfo,
      password:e.target.value
    });
    setError(null);
    let capsCount, smallCount, numberCount, symbolCount
    if (password.length < 4) {
      setError("Password must be minimum 4 characters include one UPPERCASE, lowercase, number and special character: @$! % * ? &");
      return;
    }
    else {
      capsCount = (password.match(/[A-Z]/g) || []).length
      smallCount = (password.match(/[a-z]/g) || []).length
      numberCount = (password.match(/[0-9]/g) || []).length
      symbolCount = (password.match(/\W/g) || []).length
      if (capsCount < 1) {
        setError("Must contain one UPPERCASE letter");
        return;
      }
      else if (smallCount < 1) {
        setError("Must contain one lowercase letter");
        return;
      }
      else if (numberCount < 1) {
        setError("Must contain one number");
        return;
      }
      else if (symbolCount < 1) {
        setError("Must contain one special character: @$! % * ? &");
        return;
      }
      setPassword(e.target.value);
    }
  }
  
  const [isStrength, setStrength] = useState(null);
  const dataHandler = async (childData) => {
    setStrength(childData);
  }

  // const onSubmit = async (event) => {
  //   try {
  //     event.preventDefault();
  //     event.persist();
  //     console.log(userInfo.password);
  //   } catch (error) { throw error;}
  // };

  function onSubmit(event) {
    event.preventDefault();
    if (confirmedPassword !== password) {
      setIsError("Passwords do not match");
    } else {
      // Submit the form
      console.log("Form submitted");
    }
  }


  return (
  <div className="App">
    <h1>Create a new account:</h1>
    <div className="wrapper">
      <form onSubmit={onSubmit} className="login__Form">
        <label>
          First Name:
        </label>
        <input type="text" id="firstName" name="firstName" onChange={handleName} required />
        <label>
          Last Name:
        </label>
        <input type="text" id="lastName" name="lastName" onChange={handleName} required />
        <label>
          Home Country:
        </label>
        <input type="text" id="homeCountry" name="homeCountry" onChange={handleName} required />
        <label>
          Enter your email address:
        </label>
        <input type="email" id="emailAddress" name="emailAddress" onChange={handleEmailAddress} required />
        <label>
          Enter your password:
        </label>
        <input type="password" id="password" name="password"  onChange={handleChangePassword} required />
        <label>
          Confirm your password:
        </label>
        <input type="password" id="confirmedPassword" name="confirmedPassword"  onChange={confirmPassword} required />
        <label htmlFor="password">
        </label>
        <PasswordStrengthMeter password={userInfo.password} actions={dataHandler}/>
        <button type="submit" className="gr__log__button">Create Account</button>
      </form>
    </div>
  </div>
);
}
export default App