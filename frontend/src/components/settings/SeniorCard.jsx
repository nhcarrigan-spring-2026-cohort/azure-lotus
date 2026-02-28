import styles from './SeniorCard.module.css';

export default function SeniorCard({ senior }) {
  return (
    <div className={styles.seniorCard}>
      <h2>{`${senior.firstname} ${senior.lastname}`}</h2>
      <p>Phone number: {senior.phoneNumber}</p>
    </div>
  );
}
