import { TextProps, Text as BaseText } from 'react-native';

interface ITextProps extends TextProps {
    light?: boolean;
    fontSize?: "xl" | "large" | "normal" | "small";
}

const fontSizeMap: Record<NonNullable<ITextProps["fontSize"]>, number> = {
    xl: 28,
    large: 16,
    normal: 12,
    small: 10,
}

export function Text (props: ITextProps) {
    const light = props.light ?? false;

    const fontSize = fontSizeMap[props.fontSize || 'normal'];

    return <BaseText {...props} style={{
        color: light ? '#ffffff' : '#000000',
        fontSize,
        ...(props.style as any)
    }} />;
}