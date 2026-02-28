import styles from './Button.module.css';

export default function Button({
  children,
  variant = 'primary',
  size = 'medium',
  className = '',
  onClick,
  ...props
}) {
  const buttonClass = [
    styles.btn,
    styles[`btn-${variant}`],
    styles[`btn-${size}`],
    props.disabled ? styles['btn-disabled'] : '',
    className,
  ].join(' ');

  return (
    <button className={buttonClass} onClick={onClick} {...props}>
      {children}
    </button>
  );
}
