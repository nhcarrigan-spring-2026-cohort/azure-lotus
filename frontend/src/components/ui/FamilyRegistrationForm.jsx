import './FamilyRegistrationForm.css';
import Input from './Input';
import Button from './Button';
import { IoMdEye, IoMdEyeOff } from 'react-icons/io';
import { useState } from 'react';
import {useAuthContext} from "../../context/AuthContext.jsx";
import {useMutation} from '@tanstack/react-query';
import {registerRequest} from "../../api/auth.js";
import {useNavigate} from 'react-router'

export default function FamilyRegistrationForm() {

  const navigate = useNavigate()

  const register = useMutation({
        mutationFn: registerRequest,
        onSuccess: (user) => {
            // TODO: need better user feedback, using alert for now
            alert("Account created successfully! Please login.");
            navigate('/login');
        },
        onError: (error) => {
            // TODO: frontend should show user the error, using alert for now
            console.log(`Registration failed, ${JSON.stringify(error.message)}`);
            alert(`Registration failed: ${error.message}`);
        }
    })

  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    termsCheckbox: false,
  });

  const [errors, setErrors] = useState({});
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [isConfirmPasswordVisible, setIsConfirmPasswordVisible] =
    useState(false);

  const validateForm = () => {
    let newErrors = {};

    // regex
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const nameRegex = /^[a-zA-Z\u00C0-\u00FF]+([' -][a-zA-Z\u00C0-\u00FF]+)*$/;
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required.';
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Invalid email format.';
    }

    // password and confirmPassword validation
    if (!formData.password.trim()) {
      newErrors.password = 'Password is required.';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters.';
    }

    if (!formData.confirmPassword.trim()) {
      newErrors.confirmPassword = 'Confirm password is required.';
    } else if (formData.confirmPassword !== formData.password) {
      newErrors.confirmPassword = 'Passwords do not match.';
    }

    // firstName and lastName validation
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required.';
    } else if (!nameRegex.test(formData.firstName)) {
      newErrors.firstName = 'Invalid first name format.';
    }

    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required.';
    } else if (!nameRegex.test(formData.lastName)) {
      newErrors.lastName = 'Invalid last name format.';
    }

    // phone validation
    const normalizePhone = formData.phone.replace(/[^\d+]/g, '');
    if (!normalizePhone) {
      newErrors.phone = 'Phone number is required.';
    } else if (!phoneRegex.test(normalizePhone)) {
      newErrors.phone = 'Invalid phone number format.';
    }

    // checkbox validation
    if (!formData.termsCheckbox) {
      newErrors.termsCheckbox = 'You must accept the terms and conditions.';
    }

    setErrors(newErrors);

    // return true if no errors
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, type, checked, value } = e.target;

    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const isValid = validateForm();
    if (!isValid) return;

    if (isValid) {
      await register.mutateAsync({
        firstname:formData.firstName,
        lastname: formData.lastName,
        email: formData.email,
        phoneNumber:formData.phone,
        password:formData.password,
        role:"family"
      });
    }
  };

  return (
    <div className="form-container">
      <h1 className="title">Create Family Account</h1>
      <p className="title">Sign up to manage your senior care account.</p>
      <form onSubmit={handleSubmit}>
        <div className="email-wrapper">
          <label htmlFor="email-field" className="form-label">
            Email
          </label>
          <Input
            id="email-field"
            type="email"
            name="email"
            className="form-input"
            placeholder="example@email.com"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
          />
        </div>
        <div className="password-wrapper">
          <label htmlFor="password-field" className="form-label">
            Password
          </label>
          <Input
            id="password-field"
            type={isPasswordVisible ? 'text' : 'password'}
            name="password"
            className="form-input"
            placeholder="Enter password"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
          />
          <span
            className="toggle-icon"
            onClick={() => setIsPasswordVisible(!isPasswordVisible)}
          >
            {isPasswordVisible ? <IoMdEye /> : <IoMdEyeOff />}
          </span>
        </div>
        <div className="password-wrapper">
          <label htmlFor="confirm-password-field" className="form-label">
            Confirm Password
          </label>
          <Input
            id="confirm-password-field"
            type={isConfirmPasswordVisible ? 'text' : 'password'}
            name="confirmPassword"
            className="form-input"
            placeholder="Re-enter password"
            value={formData.confirmPassword}
            onChange={handleChange}
            error={errors.confirmPassword}
          />
          <span
            className="toggle-icon"
            onClick={() =>
              setIsConfirmPasswordVisible(!isConfirmPasswordVisible)
            }
          >
            {isConfirmPasswordVisible ? <IoMdEye /> : <IoMdEyeOff />}
          </span>
        </div>
        <div id="full-name-wrapper">
          <div className="name-wrapper">
            <label htmlFor="first-name-field" className="form-label">
              First Name
            </label>
            <Input
              id="first-name-field"
              type="text"
              name="firstName"
              className="form-input"
              placeholder="First Name"
              value={formData.firstName}
              onChange={handleChange}
              error={errors.firstName}
            />
          </div>
          <div className="name-wrapper">
            <label htmlFor="last-name-field" className="form-label">
              Last Name
            </label>
            <Input
              id="last-name-field"
              type="text"
              name="lastName"
              className="form-input"
              placeholder="Last Name"
              value={formData.lastName}
              onChange={handleChange}
              error={errors.lastName}
            />
          </div>
        </div>
        <div className="phone-wrapper">
          <label
            htmlFor="phone-number-field"
            id="phone-number"
            className="form-label"
          >
            Phone Number
          </label>
          <Input
            id="phone-number-field"
            type="tel"
            name="phone"
            className="form-input"
            placeholder="(555) 123-456"
            value={formData.phone}
            onChange={handleChange}
            error={errors.phone}
          />
        </div>
        <div className="terms-and-conditions-wrapper">
          <Input
            id="terms-check"
            type="checkbox"
            name="termsCheckbox"
            className="terms-and-conditions-checkbox"
            checked={formData.termsCheckbox}
            onChange={handleChange}
            error={errors.termsCheckbox}
          />
          <label htmlFor="terms-check" className="terms-label">
            I agree to the{' '}
            <a className="terms-and-conditions-link" href="#" target="_blank">
              Terms and Conditions
            </a>
          </label>
        </div>
        <div className="submit-btn-wrapper">
          <Button type="submit" size="medium" className="create-account-btn">
            Create Account
          </Button>
        </div>
      </form>
    </div>
  );
}
