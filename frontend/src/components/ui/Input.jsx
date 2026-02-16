import './Input.css';

export default function Input({
  id,
  name,
  type = 'text',
  placeholder,
  value,
  onChange,
  error = '',
  className = '',
  containerClassName = '',
  errorClassName = '',
  ...rest
}) {
  return (
    <div className={`input-container ${containerClassName}`}>
      <input
        id={id}
        name={name}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className={`input-field ${error ? 'errored' : ''} ${className}`}
        {...rest}
      />
      {error && <span className={`error-text ${errorClassName}`}>{error}</span>}
    </div>
  );
}
