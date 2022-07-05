import { Children, PropsWithChildren } from "react";
import { View } from "react-native";

interface IStackProps {
  gap?: number;
}

export function Stack(props: PropsWithChildren<IStackProps>) {
  return (
    <>
      {Children.map(props.children, (child) => (
        <View
          style={{
            paddingVertical: (props.gap ?? 20) / 2,
          }}
        >
          {child}
        </View>
      ))}
    </>
  );
}
