import * as React from 'react';

export interface CardProps {
  children: React.ReactNode;
  variant?: 'elevated' | 'outlined' | 'filled';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  interactive?: boolean;
  selected?: boolean;
  className?: string;
  onClick?: () => void;
}

export interface CardHeaderProps {
  children: React.ReactNode;
  action?: React.ReactNode;
}

export interface CardContentProps {
  children: React.ReactNode;
}

export interface CardFooterProps {
  children: React.ReactNode;
  align?: 'left' | 'center' | 'right' | 'space-between';
}

const PADDING_MAP = {
  none: '0',
  sm: '12px',
  md: '16px',
  lg: '24px',
} as const;

const VARIANT_STYLES = {
  elevated: {
    backgroundColor: '#ffffff',
    border: 'none',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)',
  },
  outlined: {
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    boxShadow: 'none',
  },
  filled: {
    backgroundColor: '#f9fafb',
    border: 'none',
    boxShadow: 'none',
  },
} as const;

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  (
    {
      children,
      variant = 'elevated',
      padding = 'md',
      interactive = false,
      selected = false,
      className,
      onClick,
    },
    ref
  ) => {
    const [isHovered, setIsHovered] = React.useState(false);

    const baseStyles: React.CSSProperties = {
      borderRadius: '8px',
      overflow: 'hidden',
      transition: 'all 200ms ease',
      cursor: interactive ? 'pointer' : 'default',
    };

    // Dynamic styles based on state
    const interactiveStyles: React.CSSProperties = interactive
      ? {
          transform: isHovered ? 'translateY(-2px)' : 'translateY(0)',
          boxShadow: isHovered
            ? '0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06)'
            : VARIANT_STYLES[variant].boxShadow,
        }
      : {};

    const selectedStyles: React.CSSProperties = selected
      ? {
          borderColor: '#3b82f6',
          boxShadow: '0 0 0 2px rgba(59, 130, 246, 0.2)',
        }
      : {};

    const combinedStyles: React.CSSProperties = {
      ...baseStyles,
      ...VARIANT_STYLES[variant],
      ...interactiveStyles,
      ...selectedStyles,
      padding: PADDING_MAP[padding],
    };

    return (
      <div
        ref={ref}
        className={className}
        style={combinedStyles}
        onClick={interactive ? onClick : undefined}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        role={interactive ? 'button' : undefined}
        tabIndex={interactive ? 0 : undefined}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = 'Card';

export const CardHeader: React.FC<CardHeaderProps> = ({ children, action }) => {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'space-between',
        paddingBottom: '12px',
        borderBottom: '1px solid #e5e7eb',
        marginBottom: '12px',
      }}
    >
      <div
        style={{
          fontSize: '18px',
          fontWeight: 600,
          color: '#111827',
          lineHeight: 1.4,
        }}
      >
        {children}
      </div>
      {action && (
        <div style={{ marginLeft: '16px', flexShrink: 0 }}>{action}</div>
      )}
    </div>
  );
};

CardHeader.displayName = 'CardHeader';

export const CardContent: React.FC<CardContentProps> = ({ children }) => {
  return (
    <div
      style={{
        fontSize: '14px',
        color: '#4b5563',
        lineHeight: 1.6,
      }}
    >
      {children}
    </div>
  );
};

CardContent.displayName = 'CardContent';

export const CardFooter: React.FC<CardFooterProps> = ({
  children,
  align = 'right',
}) => {
  const alignmentMap = {
    left: 'flex-start',
    center: 'center',
    right: 'flex-end',
    'space-between': 'space-between',
  } as const;

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: alignmentMap[align],
        paddingTop: '16px',
        marginTop: '16px',
        borderTop: '1px solid #e5e7eb',
        gap: '8px',
      }}
    >
      {children}
    </div>
  );
};

CardFooter.displayName = 'CardFooter';
