version 1.0

workflow hello_world {
    input {
        File snakemakeFile
        File nameFile # needs to be named name.txt for this demonstration
    }

    call say_name {
        input:
            snakemakeFile = snakemakeFile,
            nameFile = nameFile
    }

    output {
        File greeting = say_name.greeting
    }
}

task say_name {
    input {
        File snakemakeFile
        File nameFile
    }

    command <<<
        cp "~{snakemakeFile}" .
        cp "~{nameFile}" .
        snakemake --cores
    >>>

    runtime {
        docker : "snakemake/snakemake"
    }

    output {
        File greeting = "greeting.txt"
    }
}