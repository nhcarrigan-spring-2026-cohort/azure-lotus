import React, { useState } from 'react';
import styles from './SeniorProfileForm.module.css';
import Input from './ui/Input';
import Textarea from './ui/Textarea';
import Button from './ui/Button';
import { useNavigate } from 'react-router-dom';

export default function SeniorProfileForm() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    address: '',
    email: '',
    phone: '',
    emergencyContactName: '',
    emergencyContactPhone: '',
    medicalInfo: '',
    frequency: 'once',
    checkInTimes: [''],
  });

  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === 'frequency') {
      let newTimes = [...formData.checkInTimes];
      if (value === 'once') {
        // keep the first time (if any)
        newTimes = newTimes.length > 0 ? [newTimes[0]] : [''];
      } else if (value === 'multiple') {
        // ensure at least one time exists
        if (newTimes.length === 0) newTimes = [''];
      }
      setFormData({ ...formData, frequency: value, checkInTimes: newTimes });
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const validateForm = () => {
    let newErrors = {};

    // regex
    const nameRegex = /^[a-zA-Z\u00C0-\u00FF]+([' -][a-zA-Z\u00C0-\u00FF]+)*$/;
    const addressRegex = /^[a-zA-Z0-9\u00C0-\u00FF\s,.'#-]{5,}$/;
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;
    const medicalInfoRegex = /^(?!\s*$).+/;

    //validations
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required.';
    } else if (!nameRegex.test(formData.firstName)) {
      newErrors.firstName =
        "Please enter a valid name. Names can include letters, hyphens, spaces, and apostrophes (e.g., O'Connor or Jean-Luc).";
    }

    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required.';
    } else if (!nameRegex.test(formData.lastName)) {
      newErrors.lastName =
        "Please enter a valid name. Names can include letters, hyphens, spaces, and apostrophes (e.g., O'Connor or Jean-Luc).";
    }

    if (!formData.address.trim()) {
      newErrors.address = 'Address is required.';
    } else if (!addressRegex.test(formData.address)) {
      newErrors.address =
        'Please enter a complete address (at least 5 characters). You can include numbers, letters, and common symbols like # or -.';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required.';
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email =
        'Please enter a valid email address (e.g., example@email.com).';
    }

    const normalizePhone = formData.phone.replace(/[^\d+]/g, '');
    if (!normalizePhone.trim()) {
      newErrors.phone = 'Phone number is required.';
    } else if (!phoneRegex.test(normalizePhone)) {
      newErrors.phone =
        'Please enter a valid phone number (e.g., +1234567890). It should be between 2 and 15 digits long.';
    }

    if (!formData.emergencyContactName.trim()) {
      newErrors.emergencyContactName = 'Emergency contact name is required.';
    } else if (!nameRegex.test(formData.emergencyContactName)) {
      newErrors.emergencyContactName =
        "Please enter a valid name. Names can include letters, hyphens, spaces, and apostrophes (e.g., O'Connor or Jean-Luc).";
    }

    if (!formData.emergencyContactPhone.trim()) {
      newErrors.emergencyContactPhone = 'Emergency contact phone is required.';
    } else if (!phoneRegex.test(formData.emergencyContactPhone)) {
      newErrors.emergencyContactPhone =
        'Please enter a valid phone number (e.g., +1234567890). It should be between 2 and 15 digits long.';
    }

    if (!formData.medicalInfo.trim()) {
      newErrors.medicalInfo =
        'This field is required. Please provide the relevant medical information, or simply fill in none.';
    }

    // validate check-in times
    let timeErrors = [];
    if (formData.frequency === 'once') {
      if (!formData.checkInTimes[0]) {
        timeErrors[0] = 'Please select a check-in time.';
      } else {
        timeErrors[0] = '';
      }
    } else if (formData.frequency === 'multiple') {
      timeErrors = formData.checkInTimes.map((time, idx) =>
        time ? '' : `Time #${idx + 1} is required.`,
      );
    }
    if (timeErrors.some((err) => err)) {
      newErrors.checkInTimes = timeErrors;
    }

    setErrors(newErrors);

    //return true if no error
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const isValid = validateForm();
    if (!isValid) return;

    console.log('Form submitted successfully:', formData);
    navigate('/invitevolunteers');
  };

  // handleTime
  const handleTimeChange = (index, value) => {
    const newTimes = [...formData.checkInTimes];
    newTimes[index] = value;
    setFormData({ ...formData, checkInTimes: newTimes });
  };

  const addTime = () => {
    if (formData.checkInTimes.length < 5) {
      setFormData({
        ...formData,
        checkInTimes: [...formData.checkInTimes, ''],
      });
    }
  };

  const removeTime = (index) => {
    if (formData.checkInTimes.length > 1) {
      const newTimes = formData.checkInTimes.filter((_, i) => i !== index);
      setFormData({ ...formData, checkInTimes: newTimes });
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Create Senior Profile</h1>
      </div>
      <form onSubmit={handleSubmit} className={styles.formContainer}>
        <fieldset className={styles.personalAndMedicalSection}>
          <legend className={styles.sectionTitle}>
            1. Senior Personal & Medical Information
          </legend>
          <div>
            <label htmlFor="firstName" className={styles.formLabel}>
              First Name
            </label>
            <Input
              type="text"
              id="firstName"
              name="firstName"
              className={styles.inputField}
              placeholder="First Name"
              value={formData.firstName}
              onChange={handleChange}
              error={errors.firstName}
              errorClassName={styles.errorTextBox}
            />
          </div>
          <div>
            <label htmlFor="lastName" className={styles.formLabel}>
              Last Name
            </label>
            <Input
              type="text"
              id="lastName"
              name="lastName"
              className={styles.inputField}
              placeholder="Last Name"
              value={formData.lastName}
              onChange={handleChange}
              error={errors.lastName}
              errorClassName={styles.errorTextBox}
            />
          </div>
          <div>
            <label htmlFor="address" className={styles.formLabel}>
              Full Address
            </label>
            <Input
              type="text"
              id="address"
              name="address"
              className={styles.inputField}
              placeholder="Enter Full Address"
              value={formData.address}
              onChange={handleChange}
              error={errors.address}
              errorClassName={styles.errorTextBox}
            />
          </div>
          <div>
            <label htmlFor="email" className={styles.formLabel}>
              Email Address
            </label>
            <Input
              type="email"
              id="email"
              name="email"
              className={styles.inputField}
              placeholder="example@email.com"
              value={formData.email}
              onChange={handleChange}
              error={errors.email}
              errorClassName={styles.errorTextBox}
            />
          </div>
          <div>
            <label htmlFor="phone" className={styles.formLabel}>
              Phone Number
            </label>
            <Input
              type="tel"
              id="phone"
              name="phone"
              className={styles.inputField}
              placeholder="Senior Phone Number"
              value={formData.phone}
              onChange={handleChange}
              error={errors.phone}
              errorClassName={styles.errorTextBox}
            />
          </div>
          <div>
            <label htmlFor="emergencyContactName" className={styles.formLabel}>
              Emergency Contact Name
            </label>
            <Input
              type="text"
              id="emergencyContactName"
              name="emergencyContactName"
              className={styles.inputField}
              placeholder="Emergency Contact Name"
              value={formData.emergencyContactName}
              onChange={handleChange}
              error={errors.emergencyContactName}
              errorClassName={styles.errorTextBox}
            />
          </div>
          <div>
            <label htmlFor="emergencyContactPhone" className={styles.formLabel}>
              Emergency Contact Phone
            </label>
            <Input
              type="tel"
              id="emergencyContactPhone"
              name="emergencyContactPhone"
              className={styles.inputField}
              placeholder="Emergency Contact Phone"
              value={formData.emergencyContactPhone}
              onChange={handleChange}
              error={errors.emergencyContactPhone}
              errorClassName={styles.errorTextBox}
            />
          </div>
          <div>
            <label htmlFor="medicalInfo" className={styles.formLabel}>
              Medical Information / Notes
            </label>
            <Textarea
              size="medium"
              rows="4"
              id="medicalInfo"
              name="medicalInfo"
              className={styles.textarea}
              placeholder="Allergies, regular medications, mobility issues..."
              value={formData.medicalInfo}
              onChange={handleChange}
              error={errors.medicalInfo}
              errorClassName={styles.errorTextBox}
            />
          </div>
        </fieldset>
        <fieldset className={styles.checkInScheduleSection}>
          <legend className={styles.sectionTitle}>2. Check-in Schedule</legend>
          <div>
            <label htmlFor="frequency">Frequency</label>
            <select
              id="frequency"
              name="frequency"
              className={styles.selectFrequency}
              value={formData.frequency}
              onChange={handleChange}
            >
              <option value="once">Once a day</option>
              <option value="multiple">Multiple times a day</option>
            </select>
          </div>
          {formData.frequency === 'once' ? (
            <div>
              <label htmlFor="checkInTime0">Daily Check-in Time</label>
              <Input
                type="time"
                id="checkInTime0"
                name="checkInTime0"
                className={styles.checkInTime}
                value={formData.checkInTimes[0] || ''}
                onChange={(e) => handleTimeChange(0, e.target.value)}
                error={errors.checkInTimes?.[0]}
                errorClassName={styles.errorTextBox}
              />
            </div>
          ) : (
            <div className={styles.multipleTimesContainer}>
              <label>Daily Check-in Times</label>
              {formData.checkInTimes.map((time, index) => (
                <div key={index} className={styles.timeInputRow}>
                  <Input
                    type="time"
                    id={`checkInTime${index}`}
                    name={`checkInTime${index}`}
                    className={styles.checkInTime}
                    containerClassName={styles.inputContainer}
                    value={time}
                    onChange={(e) => handleTimeChange(index, e.target.value)}
                    error={errors.checkInTimes?.[index]}
                    errorClassName={styles.errorTextBox}
                  />
                  {formData.checkInTimes.length > 1 && (
                    <Button
                      variant="danger"
                      size="small"
                      type="button"
                      onClick={() => removeTime(index)}
                      className={styles.removeTimeBtn}
                      aria-label={`Remove time ${index + 1}`}
                    >
                      -
                    </Button>
                  )}
                </div>
              ))}
              {formData.checkInTimes.length < 5 && (
                <Button
                  variant="secondary"
                  size="small"
                  type="button"
                  onClick={addTime}
                  className={styles.addTimeBtn}
                >
                  + Add another time
                </Button>
              )}
            </div>
          )}
        </fieldset>
        <div className={styles.submitBtnWrapper}>
          <Button type="submit">Save and Continue</Button>
        </div>
      </form>
    </div>
  );
}
