import styles from './CreateAccount.module.css';
import Input from './ui/Input';
import Button from './ui/Button';
import { IoMdEye, IoMdEyeOff } from 'react-icons/io';
import { useState } from 'react';
import { useAuthContext } from '../context/AuthContext.jsx';
import { useMutation } from '@tanstack/react-query';
import { registerRequest } from '../api/auth.js';
import { useNavigate } from 'react-router';

export default function CreateAccount() {
  const navigate = useNavigate();

  const register = useMutation({
    mutationFn: registerRequest,
    onSuccess: (user) => {
      // TODO: need better user feedback, using alert for now
      alert('Account created successfully! Please login.');
      navigate('/login');
    },
    onError: (error) => {
      // TODO: frontend should show user the error, using alert for now
      console.error(`Registration failed: ${error.data.detail}`);
      alert(`Registration failed: ${error.data.detail}`);
    },
  });

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
        firstname: formData.firstName,
        lastname: formData.lastName,
        email: formData.email,
        phoneNumber: formData.phone,
        password: formData.password,
      });
    }
  };

  return (
    <div className={styles.formContainer}>
      <h1 className={styles.title}>Create Your Account</h1>
      <p className={styles.subtitle}>
        Sign up to start connecting and monitoring wellness check-ins
      </p>
      <form onSubmit={handleSubmit}>
        <div className={styles.formGroup}>
          <label htmlFor="email-field" className={styles.formLabel}>
            Email
          </label>
          <Input
            id="email-field"
            type="email"
            name="email"
            className={styles.formInput}
            errorClassName={styles.errorTextBox}
            placeholder="example@email.com"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
          />
        </div>
        <div className={`${styles.formGroup} ${styles.passwordWrapper}`}>
          <label htmlFor="password-field" className={styles.formLabel}>
            Password
          </label>
          <Input
            id="password-field"
            type={isPasswordVisible ? 'text' : 'password'}
            name="password"
            className={styles.formInput}
            errorClassName={styles.errorTextBox}
            placeholder="Enter password"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
          />
          <button
            type="button"
            aria-label={isPasswordVisible ? 'Hide password' : 'Show password'}
            className={`${styles.toggleIcon} ${styles.resetButton}`}
            onClick={() => setIsPasswordVisible(!isPasswordVisible)}
          >
            {isPasswordVisible ? (
              <IoMdEye size="1.7em" />
            ) : (
              <IoMdEyeOff size="1.7em" />
            )}
          </button>
        </div>
        <div className={`${styles.formGroup} ${styles.passwordWrapper}`}>
          <label htmlFor="confirm-password-field" className={styles.formLabel}>
            Confirm Password
          </label>
          <Input
            id="confirm-password-field"
            type={isConfirmPasswordVisible ? 'text' : 'password'}
            name="confirmPassword"
            className={styles.formInput}
            errorClassName={styles.errorTextBox}
            placeholder="Re-enter password"
            value={formData.confirmPassword}
            onChange={handleChange}
            error={errors.confirmPassword}
          />
          <button
            type="button"
            aria-label={
              isConfirmPasswordVisible ? 'Hide password' : 'Show password'
            }
            className={`${styles.toggleIcon} ${styles.resetButton}`}
            onClick={() =>
              setIsConfirmPasswordVisible(!isConfirmPasswordVisible)
            }
          >
            {isConfirmPasswordVisible ? (
              <IoMdEye size="1.7em" />
            ) : (
              <IoMdEyeOff size="1.7em" />
            )}
          </button>
        </div>
        <div className={`${styles.formGroup} ${styles.fullNameWrapper}`}>
          <div className={styles.nameWrapper}>
            <label htmlFor="first-name-field" className={styles.formLabel}>
              First Name
            </label>
            <Input
              id="first-name-field"
              type="text"
              name="firstName"
              className={styles.formInput}
              errorClassName={styles.errorTextBox}
              placeholder="First Name"
              value={formData.firstName}
              onChange={handleChange}
              error={errors.firstName}
            />
          </div>
          <div className={styles.nameWrapper}>
            <label htmlFor="last-name-field" className={styles.formLabel}>
              Last Name
            </label>
            <Input
              id="last-name-field"
              type="text"
              name="lastName"
              className={styles.formInput}
              errorClassName={styles.errorTextBox}
              placeholder="Last Name"
              value={formData.lastName}
              onChange={handleChange}
              error={errors.lastName}
            />
          </div>
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="phone-number-field" className={styles.formLabel}>
            Phone Number
          </label>
          <Input
            id="phone-number-field"
            type="tel"
            name="phone"
            className={styles.formInput}
            errorClassName={styles.errorTextBox}
            placeholder="(555) 123-456"
            value={formData.phone}
            onChange={handleChange}
            error={errors.phone}
          />
        </div>
        <div className={styles.termsAndConditionsWrapper}>
          <Input
            id="terms-check"
            type="checkbox"
            name="termsCheckbox"
            className={styles.termsAndConditionsCheckbox}
            errorClassName={styles.errorTextBox}
            checked={formData.termsCheckbox}
            onChange={handleChange}
            error={errors.termsCheckbox}
          />
          <label htmlFor="terms-check" className={styles.termsLabel}>
            I agree to the{' '}
            <a
              className={styles.termsAndConditionsLink}
              href="#"
              target="_blank"
            >
              Terms and Conditions
            </a>
          </label>
        </div>
        <div className={styles.submitBtnWrapper}>
          <Button type="submit" size="medium">
            Create Account
          </Button>
        </div>
      </form>
    </div>
  );
}
