import Input from './ui/Input';
import Button from './ui/Button';
import styles from './InviteForm.module.css';
import { useState } from 'react';

export default function InviteForm({ onInvite }) {
  const [volunteerEmail, setVolunteerEmail] = useState('');
  const [volunteerEmailError, setVolunteerEmailError] = useState('');

  const handleChange = (e) => {
    const { value } = e.target;
    setVolunteerEmail(value);
    // clear error
    if (volunteerEmailError) setVolunteerEmailError('');
  };

  const validateForm = () => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (!volunteerEmail.trim()) {
      setVolunteerEmailError('Email is required.');
      return false;
    }
    if (!emailRegex.test(volunteerEmail)) {
      setVolunteerEmailError('Invalid email format.');
      return false;
    }

    setVolunteerEmailError('');
    return true;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const isValid = validateForm();
    if (!isValid) return;

    // send data to Parent
    if (onInvite) {
      onInvite(volunteerEmail);
    }
  };

  return (
    <form className={styles.inviteFormContainer} onSubmit={handleSubmit}>
      <h1 className={styles.title}>Invite Volunteer</h1>
      <div className={styles.inviteEmailWrapper}>
        <label htmlFor="invite-email" className={styles.formLabel}>
          Enter Volunteer Email
        </label>
        <Input
          type="email"
          name="volunteerEmail"
          id="invite-email"
          className={styles.formInput}
          containerClassName={styles.fullWidth}
          errorClassName={styles.errorTextAligned}
          placeholder="example@email.com"
          value={volunteerEmail}
          onChange={handleChange}
          error={volunteerEmailError}
        />
      </div>
      <div className={styles.buttonWrapper}>
        <Button type="submit" className={styles.sendInviteBtn}>
          Send Invite
        </Button>
      </div>
    </form>
  );
}
