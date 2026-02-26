import Button from './Button.jsx';
import styles from './CheckInButton.module.css';

export default function CheckInButton({
  variant = 'primary',
  Icon = null,
  text = '',
  subText = null,
  onClick = () => {},
}) {
  return (
    <Button
      variant={variant}
      className={styles.btn}
      size="large"
      onClick={onClick}
    >
      <div className={styles.iconTextContainer}>
        {Icon && <Icon />}
        {text}
      </div>
      {subText && <span className={styles.subText}>{subText}</span>}
    </Button>
  );
}
