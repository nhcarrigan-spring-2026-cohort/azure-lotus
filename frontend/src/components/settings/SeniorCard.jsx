import styles from './SeniorCard.module.css';

export default function SeniorCard({ senior }) {
  return (
    <div className={styles.seniorCard}>
      <h2>{`${senior.first_name} ${senior.last_name}`}</h2>
      <p>Email: {senior.email}</p>
      <p>Phone number: {senior.phone_number}</p>
    </div>
  );
}
