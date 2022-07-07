import { View, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Text } from "../components/Text"
import { LoginForm } from '../features/LoginForm';
import { utils } from '../styles/utils';

export function Login () {
    return (
        <View style={styles.welcomeView}>
            <SafeAreaView style={utils.flex}>
                <Text style={{
                    paddingLeft: 25
                }} light fontSize='xl'>Welcome!</Text>

                <View style={styles.loginView}>
                    <LoginForm />
                </View>
            </SafeAreaView>
        </View>
    )
}

const styles = StyleSheet.create({
    welcomeView: {
        flex: 1,
        backgroundColor: "#457b9d",
        paddingTop: 140,
    },
    loginView: {
        marginTop: 60,
        borderTopRightRadius: 35,
        borderTopLeftRadius: 35,
        flex: 1,
        backgroundColor: "#ffffff",
        padding: 30
    }
})