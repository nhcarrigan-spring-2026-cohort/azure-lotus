import InviteForm from '../components/InviteForm';
import styles from './InviteVolunteers.module.css';

export default function InviteVolunteers() {
  const handleInvite = (email) => {
    console.log('Parent received:', email);
  };

  return (
    <main className={styles.inviteVolunteersPage}>
      <div className={styles.contentContainer}>
        <InviteForm onInvite={handleInvite} />
      </div>
    </main>
  );
}
